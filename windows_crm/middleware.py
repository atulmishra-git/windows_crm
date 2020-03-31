from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import LANGUAGE_SESSION_KEY


class ForceLangMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if LANGUAGE_SESSION_KEY not in request.session:
            request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
            translation.activate(request.LANG)
            request.LANGUAGE_CODE = request.LANG
