import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_register_get(client):
    response = client.get(reverse("register"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_register_success(client):
    response = client.post(
        reverse("register"),
        {
            "first_name": "John",
            "last_name": "Doe",
            "username": "john",
            "email": "john@test.com",
            "password": "test123",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("home")

    assert User.objects.filter(username="john").exists()