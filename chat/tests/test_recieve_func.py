import json

from chat.consumers import ChatConsumer


def test_reciever_func_sends_json():
    consumer = ChatConsumer()

    sent_data = None

    def fake_send(data):
        # nolocal means it is the send_data outside of the function. sth like globa in django  
        nonlocal sent_data
        sent_data = data
    #  it turns send function inside of the consumer to the new function fake_send
    # now when using consumer.reciever_func(payload) it uses fake send:
    # instead of normal self.send(data)
 
    consumer.send = fake_send

    payload = {
        "type": "reciever_func",
        "data_type": "new",
        "data": "hello",
    }

    consumer.reciever_func(payload)

    assert json.loads(sent_data) == payload