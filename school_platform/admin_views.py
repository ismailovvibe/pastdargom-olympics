from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from users.models import User
from olympiads.models import Olympiad, Question, Submission
from profiles.models import Profile
from chat.models import ChatMessage
from news.models import Announcement
from django.db.models import Count, Sum, Q
from django.utils import timezone

# audit logging
from school_platform.models import AuditLog


def log_action(request, description: str):
    """Helper that creates an AuditLog entry for the current user.
    Non‑authenticated users are stored as NULL. The IP address is recorded
    when available.
    """
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=description,
        ip_address=request.META.get('REMOTE_ADDR')
    )


def admin_required(view_func):
    """Decorator ensuring the user is an authenticated staff member.

    If the user is not logged in they are redirected to the registration
    page with an informational message.  If they are logged in but not a
    staff member they are sent back to login with an error message.  This
    mirrors the behaviour the user requested in Uzbek: "account ochmasdak
    kirmoqchi bulsa acant oching".
    """
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Iltimos, avvalo hisob yarating yoki tizimga kiring.')
            return redirect('register')
        if not request.user.is_staff:
            messages.error(request, 'Admin panelga kirish uchun admin huquq kerak!')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapped_view


@login_required
@admin_required
def admin_dashboard(request):
    """Admin dashboard - asosiy sahifa"""
    
    # Statistika
    total_users = User.objects.count()
    total_olympiads = Olympiad.objects.count()
    total_submissions = Submission.objects.count()
    total_messages = ChatMessage.objects.filter(deleted=False).count()
    
    # Active olim
    active_olympiads = Olympiad.objects.filter(status='in_progress').count()
    
    # Oxirgi submissionlar
    recent_submissions = Submission.objects.select_related('user', 'question').order_by('-submitted_at')[:5]
    
    # Qo'ng'iroqlar
    announcements = Announcement.objects.all().count()
    
    context = {
        'total_users': total_users,
        'total_olympiads': total_olympiads,
        'total_submissions': total_submissions,
        'total_messages': total_messages,
        'active_olympiads': active_olympiads,
        'recent_submissions': recent_submissions,
        'announcements': announcements,
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required
@admin_required
def users_list(request):
    """Barcha foydalanuvchilar ro'yxati"""
    
    users = User.objects.all().order_by('-date_joined')
    
    # Qidiruv
    search = request.GET.get('search')
    if search:
        users = users.filter(Q(username__icontains=search) | Q(email__icontains=search))
    
    # Filter
    filter_type = request.GET.get('filter')
    if filter_type == 'admin':
        users = users.filter(is_staff=True)
    elif filter_type == 'banned':
        users = users.filter(is_banned=True)
    elif filter_type == 'active':
        users = users.filter(is_banned=False)
    
    # Profil ma'lumotlar
    for user in users:
        try:
            user.profile = Profile.objects.get(user=user)
        except:
            user.profile = None
    
    context = {'users': users, 'search': search, 'filter_type': filter_type}
    return render(request, 'admin/users_list.html', context)


@login_required
@admin_required
def edit_user(request, user_id):
    """Foydalanuvchini tahrirlash"""
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_banned = request.POST.get('is_banned') == 'on'
        user.email = request.POST.get('email', user.email)
        user.save()
        
        messages.success(request, f'{user.username} muvaffaqiyatli o\'zgartirildi!')
        log_action(request, f"Edited user {user.username} (id={user.id})")
        return redirect('custom_admin:users')
    
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = None
    
    context = {'user': user, 'profile': profile}
    return render(request, 'admin/edit_user.html', context)


@login_required
@admin_required
def delete_user(request, user_id):
    """Foydalanuvchini o'chirish"""
    
    user = get_object_or_404(User, id=user_id)
    username = user.username
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'{username} o\'chirildi!')
        log_action(request, f"Deleted user {username} (id={user_id})")
        return redirect('custom_admin:users')
    
    return render(request, 'admin/confirm_delete.html', {'object': user, 'type': 'Foydalanuvchi'})


@login_required
@admin_required
def olympiads_list(request):
    """Olimpiadalar ro'yxati"""
    
    olympiads = Olympiad.objects.annotate(
        question_count=Count('questions'),
        submission_count=Count('questions__submissions')
    ).all().order_by('-start_time')
    
    context = {'olympiads': olympiads}
    return render(request, 'admin/olympiads_list.html', context)


@login_required
@admin_required
def create_olympiad(request):
    """Yangi olimpiad yaratish"""
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status', 'open')
        duration = request.POST.get('duration_minutes', 120)
        
        olympiad = Olympiad.objects.create(
            title=title,
            description=description,
            status=status,
            duration_minutes=int(duration),
        )
        
        messages.success(request, f'"{title}" olimpiadasi yaratildi!')
        log_action(request, f"Created olympiad '{title}' (id={olympiad.id})")
        return redirect('custom_admin:questions', olympiad_id=olympiad.id)
    
    return render(request, 'admin/create_olympiad.html')


@login_required
@admin_required
def edit_olympiad(request, olympiad_id):
    """Olimpiadani tahrirlash"""
    
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    
    if request.method == 'POST':
        olympiad.title = request.POST.get('title', olympiad.title)
        olympiad.description = request.POST.get('description', olympiad.description)
        olympiad.status = request.POST.get('status', olympiad.status)
        olympiad.duration_minutes = int(request.POST.get('duration_minutes', olympiad.duration_minutes))
        olympiad.save()
        
        messages.success(request, 'Olimpiad o\'zgartirildi!')
        log_action(request, f"Edited olympiad '{olympiad.title}' (id={olympiad.id})")
        return redirect('custom_admin:olympiads')
    
    context = {'olympiad': olympiad}
    return render(request, 'admin/edit_olympiad.html', context)


@login_required
@admin_required
def delete_olympiad(request, olympiad_id):
    """Olimpiadani o'chirish"""
    
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    title = olympiad.title
    
    if request.method == 'POST':
        olympiad.delete()
        messages.success(request, f'"{title}" olimpiadasi o\'chirildi!')
        log_action(request, f"Deleted olympiad '{title}' (id={olympiad_id})")
        return redirect('custom_admin:olympiads')
    
    return render(request, 'admin/confirm_delete.html', {'object': olympiad, 'type': 'Olimpiad'})


@login_required
@admin_required
def questions_list(request, olympiad_id):
    """Savollar ro'yxati"""
    
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    questions = olympiad.questions.all()
    
    context = {'olympiad': olympiad, 'questions': questions}
    return render(request, 'admin/questions_list.html', context)


@login_required
@admin_required
def create_question(request, olympiad_id):
    """Yangi savol yaratish"""
    
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        question_type = request.POST.get('question_type', 'text')
        max_score = int(request.POST.get('max_score', 10))
        hint = request.POST.get('hint', '')
        
        question = Question.objects.create(
            olympiad=olympiad,
            text=text,
            question_type=question_type,
            max_score=max_score,
            hint=hint,
        )
        
        if question_type == 'multiple_choice':
            options = request.POST.get('mc_options', '').split('\n')
            correct = request.POST.get('mc_answer', '0')
            question.mc_options = '|'.join([o.strip() for o in options if o.strip()])
            question.mc_answer = correct
            question.save()
        
        messages.success(request, 'Savol yaratildi!')
        log_action(request, f"Created question (id={question.id}) for olympiad {olympiad.title} (id={olympiad.id})")
        return redirect('custom_admin:questions', olympiad_id=olympiad_id)
    
    context = {'olympiad': olympiad}
    return render(request, 'admin/create_question.html', context)


@login_required
@admin_required
def submissions_list(request):
    """Submissions ro'yxati"""
    
    submissions = Submission.objects.select_related('user', 'question').order_by('-submitted_at')
    
    context = {'submissions': submissions}
    return render(request, 'admin/submissions_list.html', context)


@login_required
@admin_required
def audit_logs(request):
    """List audit log entries (most recent first)."""
    logs = AuditLog.objects.select_related('user').order_by('-timestamp')
    context = {'logs': logs}
    return render(request, 'admin/audit_logs.html', context)
