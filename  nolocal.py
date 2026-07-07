

import json

class myClass():
    def send(self,data):
        pass
    def reciever_func(self, data_from_layer):
        data = json.dumps(data_from_layer)
        self.send(data)


def myf():
    mc=myClass()

    my_data=None
    def fake_send(data):
        nonlocal my_data
        my_data = data

    mc.send = fake_send
    payload = {
        "type": "reciever_func",
        "data_type": "new",
        "data": "hello",
    }

    print(my_data)
    mc.reciever_func(payload)
    print(json.loads(my_data))

myf()