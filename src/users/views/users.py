
from typing import TypeAlias, Annotated, Any

from crum import get_current_user
from django.contrib.auth import get_user_model
from djoser import permissions as djoser_permissions
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions, status, authentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as jwt_authentication

from common.views import mixins
from users.jwt.tokens import set_refresh_cookie
from users.serializers.api import users as user_s

User = get_user_model()

RegistrationSerializer: TypeAlias = user_s.RegistrationSerializer


@extend_schema_view(
    registration=extend_schema(
        summary='User registration',
        tags=['Registration'],
    ),
    change_password=extend_schema(
        summary='Change password',
        tags=['Authorization'],
    ),
    me=extend_schema(
        summary='User profile',
        tags=['User'],
    ),
    update=extend_schema(
        summary='Update user profile',
        tags=['User']),
    partial_update=extend_schema(
        summary='Partially update user profile',
        tags=['User']),

    )
class CustomUserViewSet(mixins.ExtendedUserViewSet):
    """
    User view.
    This view includes user authorization and registration.
    It also includes user information and modifications.
    """
    queryset = User.objects.all()

    authentication_classes = (jwt_authentication.JWTAuthentication,)
    multi_authentication_classes = {
        'registration': (authentication.BasicAuthentication,),
    }

    permission_classes = (djoser_permissions.CurrentUserOrAdmin,)
    multi_permission_classes = {
        'registration': (permissions.AllowAny,),
    }

    serializer_class = user_s.UserSerializer
    multi_serializer_class = {
        'registration': user_s.RegistrationSerializer,
        'change_password': user_s.ChangePasswordSerializer,
        'me': user_s.UserSerializer,
    }

    def get_object(self) -> User:
        """Retrieve the user object"""
        return self.request.user

    @action(methods=['POST'], detail=False)
    def registration(
            self, request: Request, *args: None, **kwargs: None
    ):
        """User registration method."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        response_data = {
            "user": data["user"],
            "access": data["access"]
        }

        response = Response(response_data, status=status.HTTP_201_CREATED)
        set_refresh_cookie(response, data["refresh"])

        return response


    @action(methods=['POST'], detail=False)
    def change_password(self, request: Request) -> Response:
        """Method for changing the password."""
        user = get_current_user()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":  "Password updated" },status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False)
    def me(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Method for viewing the user."""
        return self.retrieve(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        filters=True,
        summary='Search through the user list',
        tags=['Search'],
    )
)
class UserListSearchView(mixins.ListViewSet):
    """User list view."""
    permission_classes = [AllowAny]
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = user_s.UserListSearchSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('email', 'username')
    ordering = ('username', '-id')


@extend_schema_view(
    retrieve=extend_schema(summary='Get user profile by ID',
                            tags=['User']),
)
class UserRetrieveView(mixins.RetrieveListViewSet):
    """
    Retrieve user profile by ID (public).
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = user_s.UserSerializer
