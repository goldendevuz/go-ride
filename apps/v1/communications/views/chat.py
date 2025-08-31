import asyncio
import time
import json
import redis
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from apps.v1.communications.models import Chat, Message
from apps.v1.users.models import Profile
from apps.v1.communications.serializers import MessageSerializer
from apps.v1.shared.utils.sse import event_stream
from apps.v1.shared.utils.renderers import SSERenderer

r = redis.from_url(settings.REDIS_URL)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_chat(request):
    """
    Create or return existing 1-1 chat between two Profile users
    """
    other_id = (request.data.get("user_id") or "").strip()  # strip whitespace/tabs
    if not other_id:
        return Response({"error": "user_id is required"}, status=400)

    try:
        other_profile = Profile.objects.get(id=other_id)  # UUID format
    except Profile.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    # Current user profile
    user1 = request.user.profile
    user2 = other_profile

    # Always order by id to prevent duplicates
    user1, user2 = sorted([user1, user2], key=lambda u: str(u.id))
    chat, created = Chat.objects.get_or_create(user1=user1, user2=user2)
    return Response({"chat_id": str(chat.id), "created": created})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request, chat_id):
    """
    Send message in a chat (content + file + encrypted)
    """
    chat_id = str(chat_id).strip()  # clean UUID from URL
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=404)

    user_profile = request.user.profile
    if user_profile not in [chat.user1, chat.user2]:
        return Response({"error": "Not a participant"}, status=403)

    content = request.data.get("content", "")
    file = request.FILES.get("file")
    encrypted = str(request.data.get("encrypted", "false")).lower() == "true"

    message = Message.objects.create(
        chat=chat,
        sender=user_profile,
        content=content,
        file=file,
        encrypted=encrypted
    )

    serializer = MessageSerializer(message, context={"request": request})
    # Publish to Redis channel for SSE
    r.publish(f"chat:{chat_id}", json.dumps(serializer.data, default=str))
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def stream_messages(request, chat_id):
    """
    SSE endpoint to stream chat messages in real-time
    """
    chat_id = str(chat_id).strip()  # clean UUID
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=404)

    user_profile = request.user.profile
    if user_profile not in [chat.user1, chat.user2]:
        return Response({"error": "Not a participant"}, status=403)

    channel_name = f"chat:{chat_id}"
    response = StreamingHttpResponse(
        event_stream(channel_name),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    return response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_messages(request, chat_id):
    """
    List all messages in a chat (history)
    """
    try:
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        return Response({"error": "Chat not found"}, status=404)

    user_profile = request.user.profile
    if user_profile not in [chat.user1, chat.user2]:
        return Response({"error": "Not a participant"}, status=403)

    messages = Message.objects.filter(chat=chat).order_by("created")
    serializer = MessageSerializer(messages, many=True, context={"request": request})
    return Response(serializer.data)

class ChatStreamView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]  # DRF rendererni o‘chirib qo‘yamiz

    def get(self, request, chat_id):
        async def async_event_stream():
            last_id = None
            while True:
                qs = Message.objects.filter(chat_id=chat_id).order_by("-created")
                if qs.exists():
                    latest = qs.first()
                    if latest.id != last_id:
                        last_id = latest.id
                        payload = MessageSerializer(latest).data
                        yield f"data: {json.dumps(payload)}\n\n"
                await asyncio.sleep(2)

        async def adapter(gen):
            async for chunk in gen:
                yield chunk.encode()

        return StreamingHttpResponse(
            adapter(async_event_stream()),
            content_type="text/event-stream",
        )