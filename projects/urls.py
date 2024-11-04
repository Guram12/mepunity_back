from django.urls import path , include
from rest_framework import routers
from .views import ProjectViewSet , send_file_to_email , project_services_list , MinimumSpaceViewSet 
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)
router.register("minimum-space", MinimumSpaceViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('send-file/', send_file_to_email , name='upload_file'),
    path('project-services/', project_services_list, name='project_services_list'),
    # path('upload-progress/', get_upload_progress, name='get_upload_progress'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)















