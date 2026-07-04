from unittest.mock import patch
import json
import pytest

from chat.consumers import ChatConsumer
from chat.models import UserChannel


@pytest.mark.django_db
@patch("chat.consumers.async_to_sync")
def test_new_message_notifies_receiver(
    mock_async_to_sync,
    sender,
    receiver,
):
    UserChannel.objects.create(
        user=receiver,
        channel_name="receiver-channel",
    )

    consumer = ChatConsumer()

    consumer.scope = {
        "user": sender,
        "url_route": {"kwargs": {"id": receiver.id}},
    }

    consumer.receive(
        json.dumps(
            {
                "type": "new_message",
                "message": "hello",
            }
        )
    )

    assert mock_async_to_sync.called