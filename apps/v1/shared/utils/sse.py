import redis
from django.conf import settings

r = redis.from_url(settings.REDIS_URL)

def event_stream(channel_name):
    pubsub = r.pubsub()
    pubsub.subscribe(channel_name)
    
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data']
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            yield f"data: {data}\n\n"
