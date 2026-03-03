from django.contrib import admin
from .models import Announcement, AnnouncementReaction


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']


@admin.register(AnnouncementReaction)
class AnnouncementReactionAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'user', 'type', 'reacted_at']
    list_filter = ['type']
