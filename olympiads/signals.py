from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Submission
from profiles.models import Profile


@receiver(post_save, sender=Submission)
def update_profile_score(sender, instance, created, **kwargs):
    if created and not instance.is_cheating:
        # add score to user's profile
        profile, _ = Profile.objects.get_or_create(user=instance.user)
        profile.score += instance.score
        profile.save()
