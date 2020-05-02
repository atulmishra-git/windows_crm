# chat/consumers.py
import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache

from chat.models import ChatRoom, Message
from mainapp.models import User
from windows_crm.settings import DATETIME_FORMAT


def get_room(ids):
    ids.sort()
    return "_".join(ids)


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user2 = self.scope['url_route']['kwargs']['user']
        if not self.scope['user'].is_authenticated:
            # not accepting
            return
        if not User.objects.filter(id=user2):
            return
        ids = [str(self.scope['user'].id), user2]
        self.room_name = get_room(ids)
        # create chatroom if it does not exist
        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'create_room',
                'ids': ids,
            }
        )
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        msg_type = text_data_json['type']
        if msg_type == 'message':
            message = text_data_json['message']
            # save it
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type': 'save_message',
                    'message': message
                }
            )

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.scope['user'].id
                }
            )
        elif msg_type == 'read':
            # update the message read_by field
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type': 'read_message',
                    'room_name': text_data_json['room_name'],
                    'reader': self.scope['user'].id
                }
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': event['sender'],
            'room_name': self.room_name,
            'timestamp': datetime.now().strftime(DATETIME_FORMAT)
        }))

    def create_room(self, event):
        room_name = self.room_name
        ids = event['ids']
        if ChatRoom.objects.filter(name=room_name):
            return
        cr = ChatRoom.objects.create(name=self.room_name)
        for id in ids:
            cr.users.add(int(id))

    def save_message(self, event):
        room_name = self.room_name
        sender = self.scope['user']
        message = event['message']
        if not ChatRoom.objects.filter(name=room_name).exists():
            return
        room = ChatRoom.objects.get(name=room_name)
        message = Message.objects.create(room=room, sender=sender, message=message)
        # cache the last message in the room name
        # cache.set(room_name, message, 15)
        # print('cache is set for ', message.message)

    def schedule_notification(self, event):
        # schedule a notification if message remains unread
        pass

    def read_message(self, event):
        # message has been read
        reader = event['reader']
        room_name = event['room_name']
        # last_message = cache.get(room_name, None)
        # if not last_message:
        last_message = ChatRoom.objects.get(name=room_name).room_messages.last()
        last_message.read_by.add(reader)


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        pass

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        msg_type = text_data_json['type']
        if msg_type == 'message':
            message = text_data_json['message']
            # save it
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type': 'save_message',
                    'message': message
                }
            )

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.scope['user'].id
                }
            )
        elif msg_type == 'read':
            # update the message read_by field
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type': 'read_message',
                    'room_name': text_data_json['room_name'],
                    'reader': self.scope['user'].id
                }
            )

    def schedule_notification(self, event):
        # schedule a notification if message remains unread
        pass
