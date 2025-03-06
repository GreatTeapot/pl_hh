from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from common.models.mixins import InfoMixin


class Vacations(InfoMixin):
    class TypeChoices(models.TextChoices):
        FULL_TIME = 'FULL', _('Full Time')
        PART_TIME = 'PART', _('Part Time')
        REMOTE_TIME = 'REMOTE', _('Remote Time')

    title = models.CharField(
        verbose_name='Title',
        max_length=200,
        null=True,
        blank=True,
    )

    address = models.CharField(
        verbose_name='Address',
        max_length=200,
        null=True,
        blank=True,
    )

    company_name = models.CharField(
        verbose_name='Company Name',
        max_length=200,
        null=True,
        blank=True,

    )
    phone_number = PhoneNumberField(
        verbose_name='Phone Number',
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True,
    )
    type_vacation = models.CharField(
        verbose_name='Type Vacation',
        max_length=20,
        choices=TypeChoices.choices,
        null=True,
        blank=True,
    )
    requirements = models.TextField(
        verbose_name='Requirements',
        null=True,
        blank=True,
    )
    responsibilities = models.TextField(
        verbose_name='Responsibilities',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Vacation'
        verbose_name_plural = 'Vacations'

    def __str__(self) -> str:
        return f'{self.title}'
