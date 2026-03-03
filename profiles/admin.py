from django.contrib import admin
from django.utils.html import format_html
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar_preview', 'score', 'rank']
    readonly_fields = ['avatar_preview']
    fields = ['user', 'avatar', 'avatar_preview', 'bio', 'score', 'rank']

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 40px; height:40px; object-fit:cover; border-radius:50%;" />', obj.avatar.url)
        return '-'
    avatar_preview.short_description = 'Avatar'
