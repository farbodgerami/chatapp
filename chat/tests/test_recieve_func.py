import json

from chat.consumers import ChatConsumer


def test_reciever_func_sends_json():
    consumer = ChatConsumer()

    sent_data = None

    def fake_send(data):
        nonlocal sent_data
        sent_data = data

    consumer.send = fake_send

    payload = {
        "type": "reciever_func",
        "data_type": "new",
        "data": "hello",
    }

    consumer.reciever_func(payload)

    assert json.loads(sent_data) == payload