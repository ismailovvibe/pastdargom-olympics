from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets, permissions
from .models import Announcement, AnnouncementReaction
from .serializers import AnnouncementSerializer


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required

def news_list(request):
    announcements = Announcement.objects.all().order_by('-published_at')
    return render(request, 'news/list.html', {'announcements': announcements})


@login_required
def react_announcement(request, announcement_id):
    ann = get_object_or_404(Announcement, id=announcement_id)
    rtype = request.POST.get('type')
    if rtype not in (AnnouncementReaction.LIKE, AnnouncementReaction.DISLIKE):
        return JsonResponse({'error': 'invalid reaction'}, status=400)
    reaction, created = AnnouncementReaction.objects.get_or_create(
        announcement=ann, user=request.user,
        defaults={'type': rtype}
    )
    if not created:
        if reaction.type == rtype:
            reaction.delete()
            status = 'removed'
        else:
            reaction.type = rtype
            reaction.save()
            status = 'changed'
    else:
        status = 'added'
    likes = ann.reactions.filter(type=AnnouncementReaction.LIKE).count()
    dislikes = ann.reactions.filter(type=AnnouncementReaction.DISLIKE).count()
    return JsonResponse({'status': status, 'likes': likes, 'dislikes': dislikes})


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
