import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_get(client):
    response = client.get(reverse("login"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_success(client, user1):
    response = client.post(
        reverse("login"),
        {
            "username": "john",
            "password": "test123",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("home")


@pytest.mark.django_db
def test_login_wrong_password(client, user1):
    response = client.post(
        reverse("login"),
        {
            "username": "john",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 200
    assert "error" in response.context