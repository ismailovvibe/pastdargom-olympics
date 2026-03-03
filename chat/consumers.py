import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        user = self.scope.get('user')
        # require authenticated users only
        if not user or not user.is_authenticated:
            # 4003 used to signal authentication required;
            # client will display a friendly prompt.
            await self.close(code=4003)
            return
        # ban check
        if getattr(user, 'is_banned', False):
            # 4004 indicates banned user
            await self.close(code=4004)
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # save to database
        from .models import ChatMessage
        msg = ChatMessage.objects.create(
            room_name=self.room_name,
            user=self.scope['user'],
            content=message
        )

        # Send message to room group with metadata
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.scope['user'].username,
                'is_admin': self.scope['user'].is_staff,
                'timestamp': msg.timestamp.isoformat(),
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # propagate metadata as well
        await self.send(text_data=json.dumps({
            'message': event.get('message'),
            'username': event.get('username'),
            'timestamp': event.get('timestamp'),
        }))
