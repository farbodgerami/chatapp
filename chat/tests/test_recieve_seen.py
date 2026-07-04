import json
import pytest

from chat.consumers import ChatConsumer
from chat.models import Message


@pytest.mark.django_db
def test_receive_seen_marks_messages_seen(
    sender,
    receiver,
):
    message = Message.objects.create(
        sender=receiver,
        reciever=sender,
        message="test",
        has_been_seen=False,
    )

    consumer = ChatConsumer()

    consumer.scope = {
        "user": sender,
        "url_route": {"kwargs": {"id": receiver.id}},
    }

    consumer.receive(
        json.dumps(
            {
                "type": "seen",
            }
        )
    )

    message.refresh_from_db()

    assert message.has_been_seen is True