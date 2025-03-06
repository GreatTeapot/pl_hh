from django.urls import path
from .views import auth, users

urlpatterns = [
    path('auth/login/', auth.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('auth/jwt/refresh/', auth.CustomTokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/jwt/verify/', auth.CustomTokenVerifyView.as_view(), name='jwt-verify'),

    path('users/registration/', users.CustomUserViewSet.as_view({'post': 'registration'}), name='user-registration'),
    path('users/change-password/', users.CustomUserViewSet.as_view({'post': 'change_password'}), name='user-change-password'),
    path('users/me/', users.CustomUserViewSet.as_view({'get': 'me'}), name='user-profile'),
]
