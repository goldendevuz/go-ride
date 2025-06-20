from django.core.cache import cache
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from .models import Hospital, Specialty, Service, Banner, ContactUs
from .permissions import IsAdminOrReadOnly
from .serializers import (
    HospitalSerializer,
    SpecialtySerializer,
    ServiceSerializer,
    BannerSerializer,
    ContactUsSerializer,
)
from adrf import viewsets

class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'phone']
    search_fields = ['name', 'address', 'email', 'phone']
    ordering_fields = ['name', 'created_at']

    def list(self, request, *args, **kwargs):
        # filter, search, ordering paramlar bo‘lsa, caching qilmaslik tavsiya etiladi
        if request.query_params:
            return super().list(request, *args, **kwargs)

        cache_key = 'hospital_list'
        data = cache.get(cache_key)

        if not data:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 5)  # 5 daqiqa

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f'hospital_detail_{pk}'
        data = cache.get(cache_key)

        if not data:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 5)

        return Response(data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete('hospital_list')
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        pk = kwargs.get('pk')
        cache.delete(f'hospital_detail_{pk}')
        cache.delete('hospital_list')
        return response

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        response = super().destroy(request, *args, **kwargs)
        cache.delete(f'hospital_detail_{pk}')
        cache.delete('hospital_list')
        return response

class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsAdminOrReadOnly]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['duration', 'created_at']

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['order']
    search_fields = ['title', 'icon', 'url']
    ordering_fields = ['order']