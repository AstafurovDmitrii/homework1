from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
# Роли пользователей
class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('supplier', 'Supplier'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'supplier'})
    is_available = models.BooleanField(default=True)
    characteristics = models.JSONField(blank=True, null=True)  # для настраиваемых полей

    def __str__(self):
        return f"{self.name} ({self.supplier.name})"

class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.client.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"



class Supplier(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # может принимать заказы
    email = models.EmailField()

    def __str__(self):
        return self.name
    

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


# shop/models.py

class ProductAttribute(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, related_name="attributes", on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ("product", "attribute")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name} — {self.name}: {self.value}"




from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    supplier = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='products'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='attributes'
    )
    name = models.CharField(max_length=255)  # например "Цвет"
    value = models.CharField(max_length=255)  # например "Красный"

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"
