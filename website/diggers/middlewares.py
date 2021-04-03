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
