from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Image, ContactSupport, Message
from .serializers import ChatSerializer, ImageSerializer, ContactSupportSerializer, MessageSerializer

class ContactSupportViewSet(viewsets.ModelViewSet):
    queryset = ContactSupport.objects.all()
    serializer_class = ContactSupportSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_queryset(self):
        user_profile = self.request.user.profile
        # return chats where the user is either user1 or user2
        return Chat.objects.filter(user1=user_profile) | Chat.objects.filter(user2=user_profile)

    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        user2 = self.request.data.get("user2")
        serializer.save(user1=user_profile, user2_id=user2)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Message.objects.filter(chat__user1=user_profile) | Message.objects.filter(chat__user2=user_profile)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user.profile)
