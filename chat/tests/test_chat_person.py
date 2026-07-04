import pytest
from django.urls import reverse
from chat.models import Message


@pytest.mark.django_db
def test_chat_person_returns_messages(
    client,
    user1,
    user2,
    messages,
):
    client.force_login(user1)

    response = client.get(
        reverse("chat_person", kwargs={"id": user2.id})
    )

    assert response.status_code == 200

    msgs = response.context["messages"]

    assert msgs.count() == 2
    assert response.context["person"] == user2
    assert response.context["me"] == user1


@pytest.mark.django_db
def test_chat_person_marks_messages_seen(
    client,
    user1,
    user2,
):
    unseen = Message.objects.create(
        sender=user2,
        reciever=user1,
        message="new message",
        has_been_seen=False,
    )

    client.force_login(user1)

    client.get(
        reverse("chat_person", kwargs={"id": user2.id})
    )

    unseen.refresh_from_db()

    assert unseen.has_been_seen is True