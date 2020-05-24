# chat/urls.py
from django.urls import path

from . import views2

urlpatterns = [
    path('unread_rooms/', views2.unread_chat_rooms, name='unread_rooms'),
    path('room/', views2.room, name='room'),
    path('', views2.index, name='index'),
]
