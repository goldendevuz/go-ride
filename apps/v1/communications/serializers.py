from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from apps.v1.communications.models import Chat, Message, ContactSupport, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ContactSupportSerializer(TranslatableModelSerializer):
    class Meta:
        model = ContactSupport
        fields = ("id", "name", "icon", "display_order", "url")


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "user1", "user2", "created"]


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    images = ImageSerializer(many=True, read_only=True)  # ManyToManyField to global Image model

    class Meta:
        model = Message
        fields = [
            "id",
            "chat",
            "sender",
            "sender_username",
            "content",
            "encrypted",
            "images",
            "created",
        ]
        read_only_fields = ["id", "created"]

