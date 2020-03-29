# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime

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
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
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

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': event['sender'],
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
        Message.objects.create(room=room, sender=sender, message=message)
