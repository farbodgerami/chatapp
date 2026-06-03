from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message, UserChannel
from django.contrib.auth.models import User
import datetime


class ChatConsumer(WebsocketConsumer):
    # after creating  websocket object on js:
    def connect(self):

        self.accept()
        # it sends data to onmessage in js
        # self.send('{"type":"accept","status":"accepted"}')
        # print('scope: ',self.scope)
        # print(self.scope.get('session').get('my_key'))
        # print(self.scope.get('url_route') )#{'args': (), 'kwargs': {'name': 'yechi'}}
        # print(self.scope.get('url_route').get('kwargs').get('name') )
        # print(self.scope.get('user').id)
        # print(self.scope.get('session'))

        print(self.channel_layer)
        # print('saved channels in channel layer: ',self.channel_layer.channels)#{!RwMqTZkopZLs,!itgcftOpgJFM}
        # print(type(self.channel_layer))
        print('sddddddddddddddddddddddddddddddddddddddd')
        print('current channel ddddddddddddddddddddddddname: ',self.channel_name)#{!RwMqTZkopZLs}

        # create group  and add channel to the group:
        # it wont work, becouse it is sync:
        # self.channel_layer.group_add('yechi_group',self.channel_name)
        # print('saved groups: ',self.channel_layer.groups)#{}

        # to make it work:
        # async_to_sync(self.channel_layer.group_add)('yechi_group',self.channel_name)
        # print('saved groups: ',self.channel_layer.groups)#{'yechi_group':{!RwMqTZkopZLs,!itgcftOpgJFM}}

        # type is the name of the function is getting the data
        # data={'type':'reciever_func','ab':'sdf'}

        # add channel to a group:
        # async_to_sync(self.channel_layer.group_add)('test',self.channel_name)

        # send data to group:
        # async_to_sync(self.channel_layer.group_send)('test',data)

        # send data to individual channel:
        # async_to_sync(self.channel_layer.send)(self.channel_name,data)

        try:
            user_channel = UserChannel.objects.get(user=self.scope.get("user"))
            user_channel.channel_name = self.channel_name
            user_channel.save()
        except:  # noqa: E722
            user_channel = UserChannel.objects.create(
                user=self.scope.get("user"), channel_name=self.channel_name
            )

    # chat_websocket.send on js
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

    # def disconnect(self, close_code):
    #     print("connection lost")
    #     print(close_code)
    #     pass


# self.send ==> onmessage
# chat_websocket.send==>def receive