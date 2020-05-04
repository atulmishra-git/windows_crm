from datetime import datetime
from django.db import models


class ChatRoom(models.Model):
    users = models.ManyToManyField('mainapp.User', related_name='chat_rooms')
    name = models.CharField(max_length=16, unique=True, null=False)

    @classmethod
    def unread_chat_rooms(cls, user):
        reads = [
            not room.get_last_message().is_read(user)
            for room in user.chat_rooms.all() if room.get_last_message() is not None
        ]
        return sum(reads)

    def get_last_message(self):
        try:
            return self.room_messages.latest('timestamp')
        except Message.DoesNotExist:
            return None


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

    def is_read(self, by):
        if self.sender != by:
            return by in self.read_by.all()
        return True

    @property
    def is_read_by_receiver(self):
        receiver = self.room.users.exclude(id=self.sender_id).first()
        return receiver in self.read_by.all()

    def save(self, *args, **kwargs):
        if self.sender not in self.room.users.all():
            raise PermissionError("Not part of the group.")
        self.timestamp = datetime.now()
        return super().save(*args, **kwargs)
