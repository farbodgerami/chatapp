from django.contrib import admin
from .models import Message, UserChannel

 

class MessageShow(admin.ModelAdmin):
    list_display = ["sender", "reciever", "message", "date", "time", "has_been_seen"]


admin.site.register(Message, MessageShow)


class UserChannelShow(admin.ModelAdmin):
    list_display = ["user", "channel_name"]


admin.site.register(UserChannel, UserChannelShow)
