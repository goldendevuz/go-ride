from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from .models import ContactSupport, Message, Image

class ContactSupportSerializer(TranslatableModelSerializer):
    class Meta:
        model = ContactSupport
        fields = ("id", "name", "icon", "display_order", "url")

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "file", "alt_text"]


class MessageSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.user.get_full_name", read_only=True)
    receiver_name = serializers.CharField(source="receiver.user.get_full_name", read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            "id", "owner", "owner_name",
            "receiver", "receiver_name",
            "text", "images", "has_read", "created"
        ]
        read_only_fields = ["id", "created", "owner_name", "receiver_name"]