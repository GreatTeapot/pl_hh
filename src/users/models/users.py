from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers.users import CustomUserManager


class User(AbstractUser):
    """
    User model with custom roles.
    """

    class Role(models.TextChoices):
        ADMIN = 'ADM', _('Administrator')
        EMPLOYER = 'EMPLOYER', _('Employer')
        EMPLOYEE = 'EMPLOYEE', _('EMPLOYEE')
        ANONYMOUS = 'ANON', _('Anonymous')


    username = models.CharField(
        verbose_name='Username',
        max_length=32,
        unique=True,
        null=True,
        blank=True,
    )

    role = models.CharField(
        verbose_name='User Role',
        max_length=10,
        choices=Role.choices,
        default=Role.EMPLOYEE,
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        null=True,
        blank=True,
    )

    first_name = models.CharField(
        verbose_name='First Name',
        max_length=100,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        max_length=100,
        blank=True,
        null=True,
    )
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def __str__(self) -> str:
        return f'{self.username} ({self.pk})'
