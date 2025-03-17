from django.shortcuts import render
from django.views import View
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import views
from rest_framework_simplejwt.views import TokenObtainPairView
from users.jwt.tokens import set_refresh_cookie
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
import requests
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


@extend_schema_view(
    post=extend_schema(
        summary="Custom Token creation",
        tags=["Authentication"],
    ),
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Кастомный вход с установкой refresh_token в cookie"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]

        response = Response({"access": access}, status=status.HTTP_200_OK)
        set_refresh_cookie(response, refresh)

        return response

@extend_schema_view(
    post=extend_schema(
        summary='Token refresh',
        tags=['Authentication'],
    ),
)
class CustomTokenRefreshView(views.TokenRefreshView):
    """View for refreshing a token."""
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Token verification',
        tags=['Authentication'],
    ),
)
class CustomTokenVerifyView(views.TokenVerifyView):
    """View for verifying a token."""
    pass


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client
    authentication_classes = []  

class GoogleLoginCallback(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Получает код авторизации от Google, запрашивает access и refresh токены,
        затем создает и возвращает JWT access и refresh токены, которые используются в Django.
        """
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Authorization code not provided"}, status=status.HTTP_400_BAD_REQUEST)

        token_url = "https://oauth2.googleapis.com/token"

        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)
        token_data = response.json()

        if "error" in token_data:
            return Response({"error": token_data["error"]}, status=status.HTTP_400_BAD_REQUEST)

        google_access_token = token_data.get("access_token")

        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        user_info_response = requests.get(user_info_url, headers={"Authorization": f"Bearer {google_access_token}"})
        user_info = user_info_response.json()

        if "email" not in user_info:
            return Response({"error": "Failed to retrieve user info"}, status=status.HTTP_400_BAD_REQUEST)

        email = user_info["email"]
        User = get_user_model()
        user, created = User.objects.get_or_create(email=email)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({"access": str(access)}, status=status.HTTP_200_OK)
        set_refresh_cookie(response, str(refresh))

        return response


class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )