from rest_framework.routers import DefaultRouter
from vacations.views.vacations import VacationsViewSet

router = DefaultRouter()
router.register(r'vacations', VacationsViewSet, basename='vacations')

urlpatterns = router.urls
