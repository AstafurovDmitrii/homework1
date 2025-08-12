from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Product, Order, Customer, Category

# ===== Ресурсы для импорта/экспорта =====

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock', 'category__name', 'description')

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('id', 'customer__name', 'customer__email', 'total_price', 'status', 'created_at')

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'email', 'phone', 'address')

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name')

# ===== Админка с импортом/экспортом =====

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'price', 'stock', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_display = ('id', 'customer', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__name', 'customer__email')

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email')

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name',)
    search_fields = ('name',)
