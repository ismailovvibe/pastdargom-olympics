from django.test import TestCase
from django.urls import reverse
from users.models import User
from .models import ChatMessage


class ChatTests(TestCase):
    def test_room(self):
        # login/registration required: should redirect to register page
        response = self.client.get(reverse('chat_room', args=['room1']))
        self.assertRedirects(response, '/auth/register/?next=/chat/room1/')
        # after login it should work
        from users.models import User
        user = User.objects.create_user(username='msguser', password='Testpass123!')
        self.client.login(username='msguser', password='Testpass123!')
        response = self.client.get(reverse('chat_room', args=['room1']))
        self.assertEqual(response.status_code, 200)

    def test_room_shows_existing_messages(self):
        from .models import ChatMessage
        from users.models import User
        user = User.objects.create_user(username='msguser', password='Testpass123!')
        ChatMessage.objects.create(room_name='room1', user=user, content='hello')
        # must login to view
        self.client.login(username='msguser', password='Testpass123!')
        response = self.client.get(reverse('chat_room', args=['room1']))
        self.assertContains(response, 'hello')




class ChatMiddlewareTests(TestCase):
    def test_protected_paths_redirect(self):
        # visiting chat room when anonymous sends to register
        resp = self.client.get('/chat/general/')
        self.assertRedirects(resp, '/auth/register/?next=/chat/general/')
        # home page remains accessible
        resp2 = self.client.get('/')
        self.assertEqual(resp2.status_code, 200)


from asgiref.sync import async_to_sync
from channels.testing import WebsocketCommunicator
from school_platform.asgi import application


class ChatConsumerTests(TestCase):
    def test_ws_anonymous_is_denied(self):
        communicator = WebsocketCommunicator(application, "/ws/chat/room1/")
        connected, _ = async_to_sync(communicator.connect)()
        self.assertFalse(connected)
        # disconnect only if connected to avoid CancelledError
        if connected:
            async_to_sync(communicator.disconnect)()


class ChatAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='chatuser', password='Testpass123!')
        self.client.login(username='chatuser', password='Testpass123!')

    def test_anonymous_cannot_post(self):
        # log out and attempt api call
        self.client.logout()
        response = self.client.post('/api/chatmessages/', {'room_name': 'room1', 'content': 'hello'})
        self.assertEqual(response.status_code, 403)

    def test_send_message(self):
        response = self.client.post('/api/chatmessages/', {'room_name': 'room1', 'content': 'hello'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ChatMessage.objects.count(), 1)

    def test_delete_message(self):
        msg = ChatMessage.objects.create(room_name='room1', user=self.user, content='hi')
        response = self.client.delete(f'/api/chatmessages/{msg.id}/')
        self.assertEqual(response.status_code, 204)
        msg.refresh_from_db()
        self.assertTrue(msg.deleted)

    def test_ban_blocks_post(self):
        self.user.is_banned = True
        self.user.save()
        response = self.client.post('/api/chatmessages/', {'room_name': 'room1', 'content': 'hello'})
        self.assertEqual(response.status_code, 403)
