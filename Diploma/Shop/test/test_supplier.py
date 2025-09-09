import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from shop.models import Supplier


@pytest.mark.django_db
def test_supplier_toggle_orders():
    supplier_user = User.objects.create_user(username="supplier", password="12345", is_staff=True)
    supplier = Supplier.objects.create(name="Test Supplier", email="test@supplier.com", user=supplier_user)

    client = APIClient()
    client.login(username="supplier", password="12345")

    # Проверим текущее состояние
    assert supplier.accepting_orders is True

    # Делаем запрос на toggle
    response = client.post(f"/api/suppliers/{supplier.id}/toggle_orders/")
    assert response.status_code == 200
    supplier.refresh_from_db()
    assert supplier.accepting_orders is False
