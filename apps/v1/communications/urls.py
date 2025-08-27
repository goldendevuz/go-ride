from rest_framework.routers import DefaultRouter
from .views import ContactSupportViewSet

router = DefaultRouter()
router.register(
    r"contact-supports",
    ContactSupportViewSet,
    basename="contact-supports"
)

urlpatterns = router.urls