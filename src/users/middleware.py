from django.contrib.auth import get_user_model

User = get_user_model()


class SetAnonymousRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            request.user.role = "ANON"
        return self.get_response(request)
