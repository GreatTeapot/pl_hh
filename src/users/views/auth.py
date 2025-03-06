from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt import views
from rest_framework_simplejwt.views import TokenObtainPairView

from users.jwt.tokens import set_refresh_cookie


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
