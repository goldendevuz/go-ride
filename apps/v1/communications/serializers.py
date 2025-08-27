from parler_rest.serializers import TranslatableModelSerializer
from .models import ContactSupport


class ContactSupportSerializer(TranslatableModelSerializer):
    class Meta:
        model = ContactSupport
        fields = ("id", "name", "icon", "display_order", "url")
