from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mainapp import twilio_api
from itertools import chain
from django.shortcuts import render
from mainapp.models import User
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
import time
import datetime


class ChatView(TemplateView):
    template_name = 'chat/chat.html'

    def get(self, request, *args, **kwargs):
        context = {}
        all_channels = []
        channel_list = twilio_api.twilio_get_channels()

        try:
            for channel in channel_list:
                # if channel.created_by == request.user.email or channel.unique_name == request.user.username:
                all_channels.append([channel.sid, channel.unique_name])
        except:
            pass

        context['users'] = all_channels
        return render(request, self.template_name, context)


@csrf_exempt
def user_search(request):
    search = request.POST.get("search")
    get_users = []
    try:
        users = User.fetch(is_superuser=None).filter(username__icontains=search)

        for user in users:
            get_users.append([user.username, user.username])

        return JsonResponse({
            "success": True,
            "users": get_users,
        })

    except:
        return JsonResponse({
            "success": False,
            "users": get_users,
        })


@csrf_exempt
def chat_messages(request):
    get_users = []
    message_chats = []
    channel_name = ""

    user_id = request.POST.get("user_id", None)
    channel_id = request.POST.get('channel_id', None)

    if channel_id:
        channel = twilio_api.twilio_get_channels(channel_id=channel_id)
        channel_name = channel.unique_name
        message_list = twilio_api.twilio_get_channel_messages(channel_id=channel_id)

        for member in channel.members.list():
            get_users.append([member.identity, channel_id])

        for chat in message_list:
            chat_date = get_region_wise_date_time(chat.date_created)
            message_chats.append([chat.body, chat.from_, chat_date])
    else:
        channel_name = user_id
        if user_id:
            get_users.append([user_id, None])

    return JsonResponse({
        "success": True,
        "users": get_users,
        "chat": message_chats,
        "selected_channel_name": channel_name
    })


@csrf_exempt
def send_messages(request):
    message = request.POST.get('message')
    user_id = request.POST.get('user_id')
    channel_id = request.POST.get('channel_id')
    try:
        if channel_id == 'null':
            channel_response = twilio_api.twilio_create_channel(user_id)
            channel_id = channel_response[1]

        sent = twilio_api.twilio_send_message_in_channel(channel_id, message)

        return JsonResponse({
            "success": sent,
            "message": message,
            "channel_id": channel_id,
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
        })


def get_region_wise_date_time(input_date):
    offset = int(-time.timezone)
    input_date = input_date + datetime.timedelta(seconds=offset)
    new_date = (str(input_date.date().strftime('%b %d,%Y')) + " " +
                str(input_date.time().strftime("%I:%M %p")).split(".")[0])

    return new_date


class GetAccessToken(generics.GenericAPIView):
    """
    Fetch Twilio Access Token
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, identity=None):
        try:
            if not identity:
                return Response({
                    "success": False,
                    "status_code": status.HTTP_200_OK,
                    "message": "Identity is not provided!"
                })

            token = fetch_user_access_token(identity=identity)

            return Response({
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Access token fetched successfully!",
                "result": {
                    "access_token": token
                }
            })

        except Exception as e:
            print("Exception occur while sending message from admin. Error: {}".format(str(e)))
            return Response({
                "success": False,
                "message": "Something Went Wrong!"
            }, status=status.HTTP_400_BAD_REQUEST)


def fetch_user_access_token(identity='dev@admin.com'):
    # Create access token with credentials
    token = AccessToken(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_API_KEY,
                        settings.TWILIO_API_SECRET, identity=identity)

    # Create an Chat grant and add to token
    chat_grant = ChatGrant(service_sid=settings.TWILIO_SERVICE_ID)
    token.add_grant(chat_grant)

    # Return token info as JSON - token.to_jwt()
    return token.to_jwt()