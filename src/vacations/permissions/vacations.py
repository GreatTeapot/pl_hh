from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import IsAuthenticated

if TYPE_CHECKING:
    from rest_framework.request import Request
    from vacations.views.vacations import VacationsViewSet

class IsEmployee(IsAuthenticated):
    """Permission class to check if the user is the author based on their role"""

    message = (
        'You do not have permission to perform this action'
    )


    def has_permission(self, request: Request, view: VacationsViewSet ):
        """Проверка пользователя, на права доступа к представлению"""
        if (
                super().has_permission(request, view) and
                request.user.role == request.user.Role.EMPLOYER
        ):
            return True
        return bool(request.user.is_superuser)


