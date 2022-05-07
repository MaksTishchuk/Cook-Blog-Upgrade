import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateformat import DateFormat

from my_profile.models import UserProfile
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'all_users'
        self.room_group_name = f'chat_{self.room_name}'

        # Присоединение к комнате
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        # Покинуть комнату
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получение сообщения от web socket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)
        date = await self.get_time_message()

        # Отправить сообщение в группу комнаты
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'time_message': str(date),
            }
        )

    # Получить сообщение от группы комнаты
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        date = await self.get_time_message()

        # Отправить сообщение WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'time_message': str(date),
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        """ Сохранить сообщение """
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user=user)
        if user_profile.photo:
            profile_photo = user_profile.photo
        else:
            profile_photo = ''

        Message.objects.create(
            username=username,
            room=room,
            content=message,
            profile_photo=profile_photo
        )

    @sync_to_async
    def get_time_message(self):
        """ Получить дату и время сообщения """
        formatted_date = DateFormat(timezone.localtime(timezone.now())).format('H:i:s d.m.y')
        return formatted_date
