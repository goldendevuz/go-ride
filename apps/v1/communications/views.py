from rest_framework import viewsets
from .models import ContactSupport
from .serializers import ContactSupportSerializer

class ContactSupportViewSet(viewsets.ModelViewSet):
    queryset = ContactSupport.objects.all() 
    serializer_class = ContactSupportSerializer