from datetime import datetime
from django.db import models


class ChatRoom(models.Model):
    users = models.ManyToManyField('mainapp.User', related_name='chat_rooms')
    name = models.CharField(max_length=16, unique=True, null=False)


class Message(models.Model):
    timestamp = models.DateTimeField()
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    sender = models.ForeignKey('mainapp.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=512)

    def save(self, *args, **kwargs):
        if self.sender not in self.room.users.all():
            raise PermissionError("Not part of the group.")
        self.timestamp = datetime.now()
        return super().save(*args, **kwargs)
