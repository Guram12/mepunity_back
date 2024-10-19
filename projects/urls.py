from django.urls import path , include
from rest_framework import routers
from .views import ProjectViewSet , send_file_to_email
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('send-file/', send_file_to_email , name='upload_file'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)















