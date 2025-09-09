import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from shop.models import Product, Supplier


@pytest.mark.django_db
def test_create_order():
    supplier = Supplier.objects.create(name="Test Supplier", email="test@supplier.com")
    product = Product.objects.create(name="Bread", price=5, supplier=supplier)
    user = User.objects.create_user(username="buyer", password="12345")

    client = APIClient()
    client.login(username="buyer", password="12345")

    response = client.post("/api/orders/", {
        "products": [product.id]
    }, format="json")

    assert response.status_code == 201
    assert response.data["products"][0]["name"] == "Bread"
