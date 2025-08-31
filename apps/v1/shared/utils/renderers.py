from rest_framework.renderers import BaseRenderer

class SSERenderer(BaseRenderer):
    media_type = "text/event-stream"
    format = "sse"
    charset = None  # chunked bo‘lgani uchun