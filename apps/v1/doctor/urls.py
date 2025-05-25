from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.v1.doctor.views import (
    DoctorViewSet,
    FavoriteViewSet,
    HistoryViewSet,
    SecuritySettingViewSet,
    WorkingHourViewSet
)

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'histories', HistoryViewSet, basename='history')
router.register(r'security-settings', SecuritySettingViewSet, basename='securitysetting')
router.register(r'working-hours', WorkingHourViewSet, basename='workinghour')

urlpatterns = [
    path('', include(router.urls)),
]