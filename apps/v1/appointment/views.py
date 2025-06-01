from django.db.models import Q
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment, Reason, Review, Rate, ReviewLike
from .permissions import IsAppointmentOwnerOrDoctorOrAdmin
from .serializers import (
    AppointmentSerializer, ReasonSerializer,
    ReviewSerializer, RateSerializer, ReviewLikeSerializer
)

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAppointmentOwnerOrDoctorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'doctor', 'user', 'date']
    search_fields = ['full_name', 'problem']
    ordering_fields = ['date', 'time', 'status']
    ordering = ['date', 'time']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            # Admin va staff hamma appointmentlarni ko‘rishi mumkin
            return Appointment.objects.all()
        # Oddiy foydalanuvchi yoki shifokor faqat o‘z appointmentlarini ko‘radi
        return Appointment.objects.filter(Q(user=user) | Q(doctor__user=user)).distinct()

class ReasonViewSet(viewsets.ModelViewSet):
    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'appointment', 'rating', 'recommend']
    search_fields = ['text']
    ordering_fields = ['created', 'rating']

class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReviewLikeViewSet(viewsets.ModelViewSet):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer
    permission_classes = [permissions.IsAuthenticated]