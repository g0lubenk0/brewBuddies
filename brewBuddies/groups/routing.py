from django.urls import path
from groups.consumers import GroupChatConsumer

"""
WebSocket URL Patterns for Group Chat

This module defines WebSocket URL patterns for handling group chat functionality using Django Channels. WebSocket connections
to specific group chats are established through the specified URL patterns.

WebSocket URL Patterns:
- "ws/group/<int:group_id>/": Handles WebSocket connections to group chat for a specific group identified by the group_id.

Example Usage in Django's routing (routing.py):
```python
from django.urls import path
from groups.consumers import GroupChatConsumer

websocket_urlpatterns = [
    path("ws/group/<int:group_id>/", GroupChatConsumer.as_asgi()),
]
"""

websocket_urlpatterns = [
    path("ws/group/<int:group_id>/chat", GroupChatConsumer.as_asgi()),
]