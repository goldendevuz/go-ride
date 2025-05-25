from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.v1.system.views import NotificationViewSet, NotificationSettingViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'notification-settings', NotificationSettingViewSet, basename='notification-setting')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('system/', include(router.urls)),
]