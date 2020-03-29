from django.contrib.auth.decorators import login_required
from django.db.models.expressions import F, Q, Value, Subquery, OuterRef
from django.db.models.functions import Concat
from django.shortcuts import render

from chat.consumers import get_room
from chat.models import ChatRoom, Message
from mainapp.models import User


@login_required
def index(request):
    uid = request.user.id
    last_message = Subquery(Message.objects.filter(
        room_id=OuterRef('chat_room')
    ).order_by('-id').values('message')[:1])
    last_sender = Subquery(Message.objects.filter(
        room_id=OuterRef('chat_room')
    ).order_by('-id').values('sender__first_name')[:1])

    users_with_chat_room = User.objects.all().annotate(
        room_name1=Concat(F('id'), Value('_'), Value(uid)),
        room_name2=Concat(Value(uid), Value('_'), F('id'))).filter(
            Q(chat_rooms__name=F('room_name1')) | Q(chat_rooms__name=F('room_name2'))
    ).annotate(
        chat_room=F('chat_rooms__id')
    )

    users_with_chat_room_messages = users_with_chat_room.annotate(
        last_message=last_message,
        last_sender=last_sender,
    )
    context = {
        'users': users_with_chat_room_messages
    }
    return render(request, 'chat/index.html', context=context)


@login_required
def room(request, user):
    ids = [str(request.user.id), user]
    room_name = get_room(ids)
    return render(request, 'chat/room.html', {
        'room_name': user,
        'messages': list(Message.objects.filter(room__name=room_name).order_by('-id'))[:50][::-1]
    })
