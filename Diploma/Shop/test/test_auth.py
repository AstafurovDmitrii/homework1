import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    response = client.post("/api/register/", {
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_login():
    User.objects.create_user(username="testuser", password="testpass123")
    client = APIClient()
    response = client.post("/api/token/", {
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access" in response.data
