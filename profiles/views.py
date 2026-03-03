from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, permissions
from .models import Profile
from .serializers import ProfileSerializer
from .forms import ProfileForm


@login_required
def profile_view(request):
    # show user profile; create if doesn't exist
    profile, _ = Profile.objects.get_or_create(user=request.user)
    # compute rank (1-based)
    higher = Profile.objects.filter(score__gt=profile.score).count()
    profile.rank = higher + 1
    profile.save()
    # activity stats from submissions
    from olympiads.models import Submission
    total_subs = Submission.objects.filter(user=request.user).count()
    correct_subs = Submission.objects.filter(user=request.user, score__gt=0).count()
    context = {
        'profile': profile,
        'total_submissions': total_subs,
        'correct_submissions': correct_subs,
    }
    return render(request, 'profiles/profile.html', context)

@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit.html', {'form': form})


@login_required

def scoreboard(request):
    profiles = Profile.objects.order_by('-score')
    return render(request, 'profiles/scoreboard.html', {'profiles': profiles})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
