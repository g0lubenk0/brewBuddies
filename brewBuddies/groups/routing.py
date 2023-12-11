from django.urls import path
from groups.consumers import GroupChatConsumer


websocket_urlpatterns = [
    path("ws/group/<int:group_id>/", GroupChatConsumer.as_asgi()),
]