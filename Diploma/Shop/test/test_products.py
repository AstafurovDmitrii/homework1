import pytest
from rest_framework.test import APIClient
from shop.models import Product, Supplier


@pytest.mark.django_db
def test_get_products_list():
    supplier = Supplier.objects.create(name="Test Supplier", email="test@supplier.com")
    Product.objects.create(name="Milk", price=10, supplier=supplier)

    client = APIClient()
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.data[0]["name"] == "Milk"
