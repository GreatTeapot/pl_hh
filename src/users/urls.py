from django.urls import include, path, re_path
from .views import auth, users

urlpatterns = [
    path('auth/login/', auth.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh/', auth.CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/jwt/verify/', auth.CustomTokenVerifyView.as_view(), name='jwt-verify'),

    path('users/registration/', users.CustomUserViewSet.as_view({'post': 'registration'}), name='user-registration'),
    path('users/change-password/', users.CustomUserViewSet.as_view({'post': 'change_password'}), name='user-change-password'),

    path('users/me/', users.CustomUserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
    }), name='user-profile'),

    path('users/', users.UserListSearchView.as_view({'get': 'list'}), name='user-list'),

    path('users/<int:pk>/', users.UserRetrieveView.as_view({'get': 'retrieve'}), name='user-detail'),


    path("login/", auth.LoginPage.as_view(), name="login"),
    path("auth/google/", auth.GoogleLogin.as_view(), name="google_login"),
    path(
        "auth/google/callback/",
        auth.GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),


]
