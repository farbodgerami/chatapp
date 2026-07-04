import pytest
from django.contrib.auth.models import User
from chat.models import Message

 
 
from chat.models import UserChannel


@pytest.fixture
def user1():
    return User.objects.create_user(
        username="john",
        password="test123"
    )


@pytest.fixture
def user2():
    return User.objects.create_user(
        username="jane",
        password="test123"
    )


@pytest.fixture
def messages(user1, user2):
    Message.objects.create(
        sender=user1,
        reciever=user2,
        message="hello"
    )

    Message.objects.create(
        sender=user2,
        reciever=user1,
        message="hi"
    )



@pytest.fixture
def sender(db):
    return User.objects.create_user(
        username="sender",
        password="test123"
    )


@pytest.fixture
def receiver(db):
    return User.objects.create_user(
        username="receiver",
        password="test123"
    )


@pytest.fixture
def authenticated_scope(sender):
    return {
        "type": "websocket",
        "user": sender,
        "url_route": {
            "kwargs": {"id": 1}
        },
    }