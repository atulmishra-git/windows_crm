from django.http.response import JsonResponse


class IsSuperAdmin(object):
    """
    Allows access only to admin users.
    """

    def dispatch(self, request, *args, **kwargs):
        if not (request.user and request.user.is_superuser):
            return JsonResponse({'message': 'You are forbidden to take that action'},
                                status=400)
        return super().dispatch(request, *args, **kwargs)
