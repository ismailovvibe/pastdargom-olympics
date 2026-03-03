from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    # store uploaded avatar image; will require MEDIA settings
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user.username}"
