from api.spectacular.urls import urlpatterns as doc_urls
from users.urls import urlpatterns as user_urls
from vacations.urls import urlpatterns as vacations_urls

app_name = 'api'

urlpatterns = []

urlpatterns += doc_urls
urlpatterns += user_urls
urlpatterns += vacations_urls