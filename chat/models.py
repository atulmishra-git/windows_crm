from datetime import datetime
from django.db import models


class ChatRoom(models.Model):
    users = models.ManyToManyField('mainapp.User', related_name='chat_rooms')
    name = models.CharField(max_length=16, unique=True, null=False)

    def get_last_message(self):
        return self.message_set.latest('timestamp')


class Message(models.Model):
    """
    NOTE: One sender, multiple receivers
    """
    timestamp = models.DateTimeField()
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE,
                             related_name='room_messages')
    sender = models.ForeignKey('mainapp.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=512)
    read_by = models.ManyToManyField('mainapp.User', related_name='+')

    def save(self, *args, **kwargs):
        if self.sender not in self.room.users.all():
            raise PermissionError("Not part of the group.")
        self.timestamp = datetime.now()
        return super().save(*args, **kwargs)
