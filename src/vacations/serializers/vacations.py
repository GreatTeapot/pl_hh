from django.utils import timezone
from rest_framework import serializers
from vacations.models.vacations import Vacations


class CreateVacationSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра вакансий"""
    class Meta:
        model = Vacations
        fields = ['id','title', 'address', 'company_name', 'phone_number',
            'description', 'type_vacation', 'requirements', 'responsibilities',
            'created_at', 'updated_at', 'created_by', 'updated_by',]
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']



class VacationsSerializers(serializers.ModelSerializer):
    """Сериализатор для создания вакансии"""

    class Meta:
        model = Vacations
        fields = ['id','title', 'address', 'company_name', 'phone_number',
            'description', 'type_vacation', 'requirements', 'responsibilities',
            'created_at', 'updated_at', 'created_by', 'updated_by',]


class UpdateVacationSerializer(CreateVacationSerializer):
    """Сериализатор для обновления вакансии"""
    pass