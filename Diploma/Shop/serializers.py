from rest_framework import serializers
from .models import Supplier, Product, Order, OrderItem

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'is_active', 'email']

class ProductSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'supplier', 'is_available', 'characteristics']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True, source='product')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'created_at', 'is_confirmed', 'items']
        read_only_fields = ['client', 'created_at', 'is_confirmed']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order




class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["id", "name"]


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source="attribute.name", read_only=True)

    class Meta:
        model = ProductAttributeValue
        fields = ["id", "attribute", "attribute_name", "value"]


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeValueSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "is_available", "attributes"]

    def create(self, validated_data):
        attributes_data = validated_data.pop("attributes", [])
        product = Product.objects.create(**validated_data)
        for attr_data in attributes_data:
            ProductAttributeValue.objects.create(product=product, **attr_data)
        return product

    def update(self, instance, validated_data):
        attributes_data = validated_data.pop("attributes", [])
        for attr_data in attributes_data:
            attr_id = attr_data.get("id", None)
            if attr_id:
                attr_value = ProductAttributeValue.objects.get(id=attr_id, product=instance)
                attr_value.value = attr_data.get("value", attr_value.value)
                attr_value.save()
            else:
                ProductAttributeValue.objects.create(product=instance, **attr_data)
        return super().update(instance, validated_data)


from rest_framework import serializers
from .models import Product, ProductAttribute

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name", "value"]

class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "attributes"]

    def create(self, validated_data):
        attrs_data = validated_data.pop("attributes", [])
        product = Product.objects.create(**validated_data)
        for attr in attrs_data:
            ProductAttribute.objects.create(product=product, **attr)
        return product




from rest_framework import serializers
from .models import Product, ProductAttribute


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'is_active', 'attributes']
