from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message, UserChannel
from django.contrib.auth.models import User
import datetime


class ChatConsumer(WebsocketConsumer):
 
    def connect(self):

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
       
       
        text_data = json.loads(text_data)
        person_id = self.scope.get("url_route").get("kwargs").get("id")
        reciever = User.objects.get(id=person_id)
        print(reciever)
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
        data = json.dumps(data_from_layer)
        self.send(data)
 