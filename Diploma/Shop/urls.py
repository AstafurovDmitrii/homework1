from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


from django.urls import path
from .views import ProductImportView

urlpatterns = [
    path('products/import/', ProductImportView.as_view(), name='product-import'),
]


from django.urls import path
from .views import ProductImportView

urlpatterns = [
    # ... твои другие пути
    path("import-products/", ProductImportView.as_view(), name="import_products"),
]




from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductAttributeViewSet

router = DefaultRouter()
router.register(r'attributes', ProductAttributeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
