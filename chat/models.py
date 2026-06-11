from django.db import models
from django.contrib.auth.models import User
 

class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.PROTECT, default=None, related_name="messages_i_sent"
    )
    reciever = models.ForeignKey(
        User, on_delete=models.PROTECT, default=None, related_name="messages_person_got"
    )
    message = models.TextField()
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    has_been_seen = models.BooleanField(null=True, default=False)

    def __str__(self):
        return str(self.sender)


class UserChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_name = models.TextField(max_length=100)
