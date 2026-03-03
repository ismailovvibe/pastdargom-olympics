from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# rest framework
from rest_framework import viewsets, permissions
from .models import Olympiad, Question, Submission
from .serializers import OlympiadSerializer, QuestionSerializer, SubmissionSerializer


@login_required

def list_olympiads(request):
    olympiads = Olympiad.objects.all()
    return render(request, 'olympiads/list.html', {'olympiads': olympiads})



@login_required
def olympiad_questions(request, olympiad_id):
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    questions = olympiad.questions.all()
    return render(request, 'olympiads/questions.html', {'olympiad': olympiad, 'questions': questions})


class OlympiadViewSet(viewsets.ModelViewSet):
    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # check previous submission for cheating before evaluating
        question = serializer.validated_data.get('question')
        code = serializer.validated_data.get('code')
        answer_text = serializer.validated_data.get('answer_text')
        mc_choice = serializer.validated_data.get('mc_choice')
        
        # track attempt number
        attempt_count = Submission.objects.filter(
            user=self.request.user, 
            question=question
        ).count()
        attempt_num = attempt_count + 1
        
        last = None
        if question and (code or answer_text):
            last = Submission.objects.filter(user=self.request.user, question=question).order_by('-submitted_at').first()
        
        submission = serializer.save(user=self.request.user, attempt_number=attempt_num)
        
        # cheating: same code twice
        if last and last.code == code and code:
            submission.is_cheating = True
            submission.score = 0
            submission.save()
        else:
            submission.evaluate()
            # update user's profile score ONLY for first attempt
            if attempt_num == 1:
                from profiles.models import Profile
                profile, _ = Profile.objects.get_or_create(user=self.request.user)
                profile.score += submission.score
                profile.save()


@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        code = request.POST.get('code')
        answer_text = request.POST.get('answer_text')
        mc_choice = request.POST.get('mc_choice')
        
        try:
            mc_choice = int(mc_choice) if mc_choice else None
        except:
            mc_choice = None
        
        # basic validation: at least one answer must be provided
        if not code and not answer_text and mc_choice is None:
            from django.contrib import messages
            messages.error(request, "Iltimos, javob yozing yoki tanlang.")
            return render(request, 'olympiads/question_detail.html', {'question': question})

        # Track attempt number
        attempt_count = Submission.objects.filter(
            user=request.user,
            question=question
        ).count()
        attempt_num = attempt_count + 1
        
        # Create submission
        submission = Submission.objects.create(
            question=question,
            user=request.user,
            code=code,
            answer_text=answer_text,
            mc_choice=mc_choice,
            attempt_number=attempt_num
        )
        submission.evaluate()
        
        # Update profile score ONLY for first attempt
        from profiles.models import Profile
        if not submission.is_cheating and attempt_num == 1:
            profile, _ = Profile.objects.get_or_create(user=request.user)
            profile.score += submission.score
            profile.save()
        
        return redirect('submission_result', submission_id=submission.id)
    
    return render(request, 'olympiads/question_detail.html', {'question': question})


@login_required

def submission_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    # only the owner or a staff member may view
    if submission.user != request.user and not request.user.is_staff:
        return HttpResponse('Unauthorized', status=401)
    
    # Calculate percentage
    if submission.question.max_score > 0:
        percentage = int((submission.score / submission.question.max_score) * 100)
    else:
        percentage = 0
    
    return render(request, 'olympiads/submission_result.html', {
        'submission': submission,
        'percentage': percentage
    })
