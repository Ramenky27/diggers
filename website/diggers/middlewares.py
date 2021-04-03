from django.utils import timezone
from django.template.response import TemplateResponse
from django.urls import reverse


class BanManagement:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith(reverse('logout')):
            if request.user.is_authenticated and request.user.is_banned:
                return TemplateResponse(request, 'ban.html').render()

        response = self.get_response(request)
        return response


class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_user = request.user
        if current_user.is_authenticated:
            if current_user.last_activity:
                tdelta = timezone.now() - current_user.last_activity
                if tdelta.seconds > 900:
                    current_user.last_activity = timezone.now()
                    current_user.save()
            else:
                current_user.last_activity = timezone.now()
                current_user.save()

        response = self.get_response(request)
        return response
