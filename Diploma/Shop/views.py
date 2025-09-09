from rest_framework import viewsets, permissions
from .models import Supplier, Product, Order
from .serializers import SupplierSerializer, ProductSerializer, OrderSerializer

from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .tasks import send_order_email

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings

from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer
from .permissions import IsSupplier, IsCustomer

import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import Product

import pandas as pd
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Product, ProductAttribute

from rest_framework import viewsets, permissions
from .models import ProductAttribute
from .serializers import ProductAttributeSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

# Поставщики
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]  # Доступ только авторизованным


# Товары
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


# Заказы
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsSupplier()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.IsAuthenticated(), IsCustomer()]
        elif self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "customer":
            return Order.objects.filter(customer=user)
        elif user.role == "supplier":
            return Order.objects.filter(items__product__supplier=user).distinct()
        return Order.objects.all()

    def perform_create(self, serializer):
        order = serializer.save(customer=self.request.user)

        # Отправляем подтверждение на email клиента
        send_mail(
            subject="Подтверждение заказа",
            message=f"Ваш заказ #{order.id} успешно создан.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
        )

        # Отправляем накладную администратору
        send_mail(
            subject="Новый заказ для обработки",
            message=f"Новый заказ #{order.id} от {self.request.user.email}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
        )


# Дополнительные действия для поставщиков
class SupplierProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplier]

    def get_queryset(self):
        return Product.objects.filter(supplier=self.request.user)

    @action(detail=False, methods=["post"])
    def toggle_orders(self, request):
        """Включить или отключить приём заказов"""
        supplier = request.user
        supplier.accepting_orders = not supplier.accepting_orders
        supplier.save()
        return Response({"accepting_orders": supplier.accepting_orders})


class ProductImportView(APIView):
    permission_classes = [IsAdminUser]  # только админы

    def post(self, request):
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response({"error": "Файл не найден"}, status=status.HTTP_400_BAD_REQUEST)

        # проверка формата файла
        if not csv_file.name.endswith(".csv"):
            return Response({"error": "Нужен CSV-файл"}, status=status.HTTP_400_BAD_REQUEST)

        # читаем CSV
        try:
            decoded_file = csv_file.read().decode("utf-8")
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            products_created = 0
            for row in reader:
                Product.objects.create(
                    name=row["name"],
                    price=row["price"],
                    quantity=row["quantity"]
                )
                products_created += 1

            return Response({"message": f"Импортировано {products_created} товаров"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [permissions.IsAdminUser]


router.register(r'attributes', ProductAttributeViewSet)


class ProductImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not request.user.is_staff and not request.user.is_supplier:
            return Response({"error": "Нет прав на импорт товаров"}, status=status.HTTP_403_FORBIDDEN)

        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Файл не передан"}, status=status.HTTP_400_BAD_REQUEST)

        filename = file.name.lower()

        # CSV
        if filename.endswith(".csv"):
            data = file.read().decode("utf-8")
            reader = csv.DictReader(io.StringIO(data))
            rows = list(reader)

        # Excel
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file)
            rows = df.to_dict(orient="records")

        else:
            return Response({"error": "Неподдерживаемый формат"}, status=status.HTTP_400_BAD_REQUEST)

        for row in rows:
            product, _ = Product.objects.update_or_create(
                name=row.get("name"),
                defaults={
                    "description": row.get("description", ""),
                    "price": row.get("price", 0),
                }
            )

            # Очистим старые характеристики и создадим новые
            product.attributes.all().delete()
            for key, value in row.items():
                if key not in ["name", "description", "price"] and value:
                    ProductAttribute.objects.create(
                        product=product,
                        name=key,
                        value=value
                    )

        return Response({"status": "Импорт завершён"}, status=status.HTTP_200_OK)


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Поставщик или админ может добавить атрибут
        return serializer.save()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        # Письмо клиенту
        send_order_email.delay(
            order.customer.email,
            "Ваш заказ оформлен",
            f"Спасибо за заказ #{order.id}!"
        )
        # Письмо админу
        send_order_email.delay(
            "admin@example.com",
            "Новый заказ",
            f"Создан новый заказ #{order.id} от {order.customer.email}"
        )

class CrashTestView(APIView):
    def get(self, request):
        division_by_zero = 1 / 0
        return Response({"status": "ok"})
    
class TestErrorView(APIView):
    def get(self, request):
        division_by_zero = 1 / 0  # вызовет ошибку
        return Response({"result": division_by_zero}, status=status.HTTP_200_OK)
    



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Кэшируем список товаров на 60 секунд
    @method_decorator(cache_page(60 * 1))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

@method_decorator(cache_page(60 * 5))  # кэшируем на 5 минут
def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)
