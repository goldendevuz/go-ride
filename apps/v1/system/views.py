from rest_framework import permissions, filters
# from django_filters.rest_framework import DjangoFilterBackend

from apps.v1.system.models import Notification, NotificationSetting, Payment
from apps.v1.system.permissions import NotificationPermission, NotificationSettingPermission, PaymentPermission
from apps.v1.system.serializers import NotificationSerializer, NotificationSettingSerializer, PaymentSerializer
from adrf import viewsets

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, NotificationPermission]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['state', 'send_at']
    search_fields = ['title', 'description']
    ordering_fields = ['send_at', 'title']
    ordering = ['-send_at']

    def perform_create(self, serializer):
        # Agar kerak bo'lsa, qo'shimcha ma'lumotlar bilan saqlash mumkin
        serializer.save()

class NotificationSettingViewSet(viewsets.ModelViewSet):
    queryset = NotificationSetting.objects.all()
    serializer_class = NotificationSettingSerializer
    permission_classes = [permissions.IsAuthenticated, NotificationSettingPermission]

    def get_queryset(self):
        # Faqat o'z foydalanuvchining sozlamalarini ko'rsatish uchun
        user = self.request.user
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, PaymentPermission]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'method', 'user']
    search_fields = ['notes', 'method']
    ordering_fields = ['amount', 'reviewed_at', 'status']
    ordering = ['-reviewed_at']

    def get_queryset(self):
        user = self.request.user
        # Agar foydalanuvchi staff bo'lsa, hamma to'lovlarni ko'rsatish mumkin, aks holda faqat o'zlarini
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(reviewed_by=self.request.user)