from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.config import API_V1_URL
from core.settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path(API_V1_URL + 'user/', include('apps.v1.user.urls')),
    path(API_V1_URL + 'doctor/', include('apps.v1.doctor.urls')),
    path(API_V1_URL + 'clinic/', include('apps.v1.clinic.urls')),
    path(API_V1_URL + 'appointment/', include('apps.v1.appointment.urls')),
    path(API_V1_URL + 'system/', include('apps.v1.system.urls')),
    path(API_V1_URL + 'api-auth/', include('rest_framework.urls')),
    path('schema-viewer/', include('schema_viewer.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)