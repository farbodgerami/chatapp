import pytest

from chat.consumers import ChatConsumer
from chat.models import UserChannel


@pytest.mark.django_db
def test_connect_updates_existing_channel(sender):
    UserChannel.objects.create(
        user=sender,
        channel_name="old-channel",
    )

    consumer = ChatConsumer()

    consumer.scope = {
        "user": sender,
        "url_route": {"kwargs": {"id": sender.id}},
    }

    consumer.channel_name = "new-channel"

    consumer.accept = lambda: None

    consumer.connect()

    channel = UserChannel.objects.get(user=sender)

    assert channel.channel_name == "new-channel"