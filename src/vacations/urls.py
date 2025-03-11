from django.urls import path
from rest_framework.routers import DefaultRouter
from vacations.views.vacations import VacationsViewSet, MyVacationsViewSet

router = DefaultRouter()
router.register(r'vacations', VacationsViewSet, basename='vacations')

urlpatterns = router.urls

urlpatterns += [
    path('vacations-me/', MyVacationsViewSet.as_view({'get': 'list'}), name='my-vacations'),
]
