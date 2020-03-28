from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from chat.consumers import get_room
from chat.models import ChatRoom, Message
from mainapp.models import User


@login_required
def index(request):
    context = {
        'users': User.objects.exclude(id=request.user.id)
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
