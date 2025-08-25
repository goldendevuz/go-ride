from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    HospitalViewSet,
    SpecialtyViewSet,
    ServiceViewSet,
    BannerViewSet,
    ContactUsViewSet,
)

router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet)
router.register(r'specialties', SpecialtyViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'banners', BannerViewSet)
router.register(r'contacts', ContactUsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]