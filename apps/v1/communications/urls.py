from rest_framework.routers import DefaultRouter
from .views import ContactSupportViewSet, MessageViewSet

router = DefaultRouter()
router.register(
    r"contact-supports",
    ContactSupportViewSet,
    basename="contact-supports"
)
router.register(r"messages", MessageViewSet, basename="messages")

urlpatterns = router.urls