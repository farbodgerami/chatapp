from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("websocket/<int:id>", consumers.ChatConsumer.as_asgi()),
]
