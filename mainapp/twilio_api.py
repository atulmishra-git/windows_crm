from django.conf import settings
from twilio.rest import Client


client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def twilio_create_channel(unique_name):
    try:
        service = client.chat.services(settings.TWILIO_SERVICE_ID).fetch()
        if service:
            try:
                channel = client.chat.services(settings.TWILIO_SERVICE_ID).channels(unique_name).fetch()
                return service.sid, channel.sid
            except Exception as e:
                channel = client.chat.services(settings.TWILIO_SERVICE_ID).channels.create(unique_name=unique_name)
                return service.sid, channel.sid
        else:
            print("Twilio Service-Id not found ")
            return False

    except Exception as e:
        print("Exception occur while fetching or creating channel. Error {}".format(str(e)))
        return False


def twilio_get_channel_member(request, service_id, channel_id, user_id, message_text):
    try:
        try:
            member = client.chat.services(service_id).channels(channel_id).members(user_id).fetch()
        except Exception as e:
            client.chat.services(service_id).channels(channel_id).members.create(identity=user_id)

        client.chat.services(service_id).channels(channel_id).messages.create(body=message_text)

    except Exception as e:
        print("Exception occur while getting channel member. Error: {}".format(str(e)))
        return False


def twilio_get_channel_messages(channel_id):
    try:
        messages = []
        try:
            messages = client.chat.services(settings.TWILIO_SERVICE_ID).channels(channel_id).messages.list()
        except Exception as e:
            pass

        return messages

    except Exception as e:
        print("Exception occur while getting channel member")
        return False


def twilio_get_channels(channel_id=None):
    channels = []
    try:
        if channel_id:
            channels = client.chat.services(settings.TWILIO_SERVICE_ID).channels(channel_id).fetch()
        else:
            channels = client.chat.services(settings.TWILIO_SERVICE_ID).channels.list()

    except Exception as e:
        print("Exception occur while getting channel member")

    return channels


def twilio_send_message_in_channel(channel_id, message):
    try:
        channel = client.chat.services(settings.TWILIO_SERVICE_ID).channels(channel_id).fetch()
        channel.messages.create(body=message)
        return True

    except Exception as e:
        print("Exception occur while sending message in channel. Error:{}".format(e))
        return False