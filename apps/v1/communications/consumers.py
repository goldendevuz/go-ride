import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.apps import apps


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Parse sender & receiver UUIDs from query string
        query_string = self.scope["query_string"].decode("utf-8")
        query_params = dict(x.split("=") for x in query_string.split("&") if "=" in x)
        sender_id = query_params.get("sender")
        receiver_id = query_params.get("receiver")

        if not sender_id or not receiver_id:
            await self.close()
            return

        self.sender_id = sender_id
        self.receiver_id = receiver_id

        # Fetch Profile objects
        Profile = apps.get_model("users", "Profile")
        try:
            self.sender = await sync_to_async(Profile.objects.get)(id=self.sender_id)
            self.receiver = await sync_to_async(Profile.objects.get)(id=self.receiver_id)
        except Profile.DoesNotExist:
            await self.close()
            return

        # Room name based on sorted user IDs (so both sides join the same room)
        user_ids = sorted([self.sender_id, self.receiver_id])
        self.room_group_name = f"user_chat_{user_ids[0]}_{user_ids[1]}"

        # Join the room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Try parsing JSON first
        try:
            data = json.loads(text_data)
            text = data.get("text")
        except json.JSONDecodeError:
            text = text_data  # fallback to plain text

        if not text:
            return

        # Save the message
        Message = apps.get_model("communications", "Message")
        from .serializers import MessageSerializer

        message = Message(owner=self.sender, receiver=self.receiver)
        message.set_current_language("en")
        message.text = text
        await sync_to_async(message.save)()

        serialized = MessageSerializer(message).data

        # Broadcast to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": serialized},
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))
