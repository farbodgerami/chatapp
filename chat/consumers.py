from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message, UserChannel
from django.contrib.auth.models import User
import datetime


class ChatConsumer(WebsocketConsumer):
    """
    WebSocket consumer responsible for handling real-time chat communication
    between authenticated users.

    This consumer manages the lifecycle of a WebSocket connection, keeps track
    of the channel associated with the connected user, processes incoming chat
    messages, stores messages in the database, and notifies the recipient in
    real time through Django Channels.

    The consumer supports two types of incoming messages:

    - ``new_message``:
        Saves a new message to the database and sends the message to the
        recipient's active WebSocket channel, if one exists.

    - ``seen``:
        Notifies the recipient that messages have been seen and marks all
        messages sent by that recipient to the current user as seen.

    Attributes:
        channel_name (str):
            The unique channel name assigned to the current WebSocket
            connection.
        scope (dict):
            Connection information provided by Django Channels, including
            the authenticated user and URL parameters.
    """
 
    def connect(self):
        """
        Accept the WebSocket connection and register the user's channel.

        If a ``UserChannel`` record already exists for the authenticated user,
        its channel name is updated to the current WebSocket channel.
        Otherwise, a new ``UserChannel`` record is created.
        """

        self.accept()
       
        try:
            user_channel = UserChannel.objects.get(user=self.scope.get("user"))
            user_channel.channel_name = self.channel_name
            user_channel.save()
        except:   
            user_channel = UserChannel.objects.create(
                user=self.scope.get("user"), channel_name=self.channel_name
            )

    
    def receive(self, text_data=None, bytes_data=None):
        """
        Process incoming WebSocket messages.

        The message is expected to be a JSON-encoded object containing a
        ``type`` field. The recipient is determined from the ``id`` URL
        parameter.

        Supported message types:

        ``new_message``:
            Creates and stores a new ``Message`` instance and sends the
            message to the recipient's WebSocket channel if the recipient
            currently has a registered channel.

        ``seen``:
            Sends a notification to the recipient and marks messages received
            from that recipient as seen.

        Args:
            text_data (str, optional):
                JSON-encoded data received through the WebSocket.
            bytes_data (bytes, optional):
                Binary data received through the WebSocket.
        """
       
       
        text_data = json.loads(text_data)
        person_id = self.scope.get("url_route").get("kwargs").get("id")
        reciever = User.objects.get(id=person_id)

        if text_data.get("type") == "new_message":

            Message.objects.create(
                sender=self.scope.get("user"),
                reciever=reciever,
                message=text_data.get("message"),
            )
            try:
                other_side_channel = UserChannel.objects.get(user=reciever)
                data = {
                    "type": "reciever_func",
                    "data_type": "new",
                    "data": text_data.get("message"),
                }

                async_to_sync(self.channel_layer.send)(
                    other_side_channel.channel_name, data
                )

            except:
                pass

        elif text_data.get("type") == "seen":

            other_side_channel = UserChannel.objects.get(user=reciever)
            data = {
                "type": "reciever_func",
                "data_type": "seen",
            }

            async_to_sync(self.channel_layer.send)(
                other_side_channel.channel_name, data
            )

            not_seen_messages = Message.objects.filter(
                sender=reciever, reciever=self.scope.get("user")
            )
            print(not_seen_messages)
            not_seen_messages.update(has_been_seen=True)

    def reciever_func(self, data_from_layer):
        """
        Send a message received from the Django Channels layer to the client.

        The data received from another channel is serialized to JSON and sent
        through the current WebSocket connection.

        Args:
            data_from_layer (dict):
                Data received from the channel layer containing information
                about the event that should be forwarded to the client.
        """
        data = json.dumps(data_from_layer)
        self.send(data)
 