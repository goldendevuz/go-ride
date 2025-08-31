from django.urls import path
from apps.v1.communications import views

urlpatterns = [
    path("chat/create/", views.create_chat, name="create_chat"),
    path("chat/<uuid:chat_id>/send/", views.send_message, name="send_message"),
    # path("chat/<uuid:chat_id>/stream/", views.stream_messages, name="stream_messages"),
    path("chat/<uuid:chat_id>/stream/", views.ChatStreamView.as_view(), name="chat-stream"),
    path("chat/<uuid:chat_id>/messages/", views.list_messages, name="list_messages"),  # 🆕
]
