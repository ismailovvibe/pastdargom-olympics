from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from asgiref.sync import sync_to_async
from django.views.decorators.http import require_http_methods

from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.filter(deleted=False)
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # prevent banned users from posting
        if self.request.user.is_banned:
            raise PermissionDenied("You are banned from chat")
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # soft delete so admins can remove
        instance.deleted = True
        instance.save()


@login_required
@require_http_methods(["GET"])
def chat_room(request, room_name):
    messages = ChatMessage.objects.filter(room_name=room_name, deleted=False).order_by('timestamp')
    return render(request, 'chat/room.html', {'room_name': room_name, 'messages': messages})
