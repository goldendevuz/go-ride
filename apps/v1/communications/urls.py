from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, ImageViewSet, ContactSupportViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"chats", ChatViewSet, basename="chat")
router.register(r"images", ImageViewSet, basename="image")
router.register(r"contacts", ContactSupportViewSet, basename="contactsupport")
router.register(r"messages", MessageViewSet, basename="message")

urlpatterns = router.urls
