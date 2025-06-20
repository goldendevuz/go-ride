from django.db.models import Q
from rest_framework import permissions, filters
# from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment, Reason, Review, Rate, ReviewLike
from .permissions import IsAppointmentOwnerOrDoctorOrAdmin
from .serializers import (
    AppointmentSerializer, ReasonSerializer,
    ReviewSerializer, RateSerializer, ReviewLikeSerializer
)
from adrf import viewsets

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAppointmentOwnerOrDoctorOrAdmin]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'doctor', 'user', 'date']
    search_fields = ['full_name', 'problem']
    ordering_fields = ['date', 'time', 'status']
    ordering = ['date', 'time']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(
            Q(user=user) | Q(doctor__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReasonViewSet(viewsets.ModelViewSet):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'appointment', 'rating', 'recommend']
    search_fields = ['text']
    ordering_fields = ['created', 'rating']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewLikeViewSet(viewsets.ModelViewSet):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)