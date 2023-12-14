"""
Module: consumers.py
Description: Defines a Django Channels consumer for handling group chat functionality using WebSocket connections.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GroupChatConsumer(AsyncWebsocketConsumer):
    """
    Represents a consumer for handling WebSocket connections related to group chat.

    Attributes:
    - group_id (str): The unique identifier of the group associated with the WebSocket connection.
    - group_name (str): The name of the group, constructed as 'group_' + group_id.
    """
    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        Adds the consumer to the group based on the provided group_id.
        """
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f"group_{self.group_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        Removes the consumer from the associated group.
        """
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Called when a message is received from the WebSocket.
        Broadcasts the received message to all members of the associated group.
        """
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group.message',
                'message': message,
                'username': self.scope['user'].username,
            }
        )

    async def group_message(self, event):
        """
        Called when a message is broadcasted to the group.
        Sends the message to the consumer's WebSocket.
        """
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
