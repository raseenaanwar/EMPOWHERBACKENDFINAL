# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.user = self.scope['user']

        # Check if the user is authenticated
        if not self.user.is_authenticated:
            await self.close()
            return

        # Join chat group
        await self.channel_layer.group_add(
            self.chat_id,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard(
            self.chat_id,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        # Save message to the database
        await self.save_message(message_text)

        # Send message to the chat group
        await self.channel_layer.group_send(
            self.chat_id,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': self.user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async
    def save_message(self, message_text):
        chat = Chat.objects.get(id=self.chat_id)
        Message.objects.create(
            chat=chat,
            sender=self.user,
            message_text=message_text
        )
