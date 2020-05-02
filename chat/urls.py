# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('unread_rooms/', views.unread_chat_rooms, name='unread_rooms'),
    path('<str:user>/', views.room, name='room'),
    path('', views.index, name='index'),
]
