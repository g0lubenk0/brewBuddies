# your_app/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import GroupChatConsumer

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/group/<int:group_id>/", GroupChatConsumer.as_asgi()),
            ]
        )
    ),
})
