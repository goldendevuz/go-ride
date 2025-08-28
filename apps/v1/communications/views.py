from rest_framework import viewsets
from .models import ContactSupport, Message
from .serializers import ContactSupportSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated

class ContactSupportViewSet(viewsets.ModelViewSet):
    queryset = ContactSupport.objects.all() 
    serializer_class = ContactSupportSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.profile
        return (Message.objects.filter(owner=user) | Message.objects.filter(receiver=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.profile)
