import json
import pytest

from chat.consumers import ChatConsumer
from chat.models import Message


@pytest.mark.django_db
def test_receive_new_message_creates_message(
    sender,
    receiver,
):
    consumer = ChatConsumer()

    consumer.scope = {
        "user": sender,
        "url_route": {"kwargs": {"id": receiver.id}},
    }

    consumer.receive(
        json.dumps(
            {
                "type": "new_message",
                "message": "hello world",
            }
        )
    )

    msg = Message.objects.get()

    assert msg.sender == sender
    assert msg.reciever == receiver
    assert msg.message == "hello world"