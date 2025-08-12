from auditlog.registry import auditlog
from .models import Product, Order, Customer

auditlog.register(Product)
auditlog.register(Order)
auditlog.register(Customer)
