from django.http import JsonResponse
from django.conf import settings
from rest_framework import status

class AndroidIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        android_id = request.headers.get('X-Android-ID')

        if android_id != settings.SECRET_KEY_ANDROID_ID:
            return JsonResponse(
                {"detail": "App no autorizada."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        response = self.get_response(request)
        return response