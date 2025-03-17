from rest_framework.response import Response

from config import settings


def set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """Устанавливает refresh_token в HttpOnly cookie"""
    response.set_cookie(
        key=settings.SIMPLE_JWT.get('REFRESH_COOKIE', 'refresh_token'),
        value=refresh_token,
        httponly=True,
        secure=False,  # Меняйте на True в продакшене
        samesite='Lax',
    )
