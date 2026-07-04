import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_logout(client, user1):
    client.force_login(user1)

    response = client.get(reverse("logout"))

    assert response.status_code == 302
    assert response.url == reverse("main")