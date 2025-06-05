from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.v1.doctor.models import Doctor, Favorite, History, SecuritySetting, WorkingHour
from apps.v1.doctor.permissions import IsOwnerOrAdmin
from apps.v1.doctor.serializers import (
    DoctorSerializer,
    FavoriteSerializer,
    HistorySerializer,
    SecuritySettingSerializer,
    WorkingHourSerializer
)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialty', 'hospital']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'about']
    ordering_fields = ['rating', 'review_count']
    ordering = ['-rating']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'doctor']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Favorite.objects.all()
        return Favorite.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['doctor']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

class SecuritySettingViewSet(viewsets.ModelViewSet):
    queryset = SecuritySetting.objects.all()
    serializer_class = SecuritySettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return SecuritySetting.objects.all()
        return SecuritySetting.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class WorkingHourViewSet(viewsets.ModelViewSet):
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['doctor', 'day_of_week']
    ordering_fields = ['day_of_week', 'start_time']
    ordering = ['day_of_week', 'start_time']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return WorkingHour.objects.all()
        return WorkingHour.objects.filter(doctor__user=user)