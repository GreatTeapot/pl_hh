from rest_framework import permissions, filters
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.db.models import Q
from rest_framework.permissions import AllowAny, IsAuthenticated
from vacations.serializers.vacations import VacationsSerializers, CreateVacationSerializer, UpdateVacationSerializer
from common.views.mixins import CRUDListViewSet, ListViewSet
from vacations.models import Vacations
from vacations.permissions.vacations import IsEmployee
from rest_framework_simplejwt import authentication as jwt_authentication
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied



@extend_schema_view(
    list=extend_schema(summary="Get vacations", tags=["Vacations"]),
    retrieve=extend_schema(summary="Get vacation by id", tags=["Vacations"]),
    create=extend_schema(summary="Create Vacation", tags=["Vacations"]),
    update=extend_schema(summary="Update Vacation", tags=["Vacations"]),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="Delete Vacations", tags=["Vacations"]),
)
class VacationsViewSet(CRUDListViewSet):
    """Views for Vacations """
    queryset = Vacations.objects.all()
    authentication_classes = (jwt_authentication.JWTAuthentication,)


    multi_permission_classes = {
        'create': (IsEmployee,),
        'update': (IsEmployee,),
        'destroy': (IsEmployee,),
        

    }
    serializer_class = VacationsSerializers
    multi_serializer_class = {
        'create': CreateVacationSerializer,
        'update': UpdateVacationSerializer,

    }
    http_method_names = ('get', 'post', 'put', 'delete')

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['company_name', 'title']
    ordering_fields = ['created_at', 'company_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(company_name__icontains=search_query)
            )
        return queryset
    
    def perform_update(self, serializer):
        """Разрешает обновление только создателю вакансии"""
        vacation = self.get_object()
        if vacation.created_by != self.request.user:
            raise PermissionDenied("Вы можете редактировать только свои вакансии.")
        serializer.save()

    def perform_destroy(self, instance):
        """Разрешает удаление только создателю вакансии"""
        if instance.created_by != self.request.user:
            raise PermissionDenied("Вы можете удалять только свои вакансии.")
        instance.delete()



@extend_schema_view(
    list=extend_schema(
        summary="Get vacations",
        tags=["Vacations"]),
)
class MyVacationsViewSet(ListViewSet):
    """Выводит список вакансий, созданных текущим пользователем"""
    queryset = Vacations.objects.all()
    serializer_class = VacationsSerializers
    authentication_classes = (jwt_authentication.JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_queryset(self):
        """Фильтруем вакансии по текущему пользователю"""
        return Vacations.objects.filter(created_by=self.request.user)
