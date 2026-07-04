import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_requires_authentication(client):
    response = client.get(reverse("home"))

    assert response.status_code == 302
    assert response.url == reverse("main")


@pytest.mark.django_db
def test_home_authenticated(client, user1, user2):
    client.force_login(user1)

    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert response.context["user"] == user1
    assert user2 in response.context["users"]