from rest_framework import serializers
from apps.v1.communications.models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "user1", "user2", "created"]


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", "chat", "sender", "sender_username", "content", "file", "file_url", "encrypted", "created"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if obj.file:
            return request.build_absolute_uri(obj.file.url)
        return None
