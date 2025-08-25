from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AppointmentViewSet, ReasonViewSet,
    ReviewViewSet, RateViewSet, ReviewLikeViewSet
)

router = DefaultRouter()
router.register('appointments', AppointmentViewSet, basename='appointment')
router.register('reasons', ReasonViewSet, basename='reason')
router.register('reviews', ReviewViewSet, basename='review')
router.register('rates', RateViewSet, basename='rate')
router.register('review-likes', ReviewLikeViewSet, basename='reviewlike')

urlpatterns = [
    path('', include(router.urls)),
]