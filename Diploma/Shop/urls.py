from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductAttributeViewSet
from django.urls import path
from .views import ProductImportView

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from django.urls import path
from .views import TestErrorView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('products/import/', ProductImportView.as_view(), name='product-import'),
]

urlpatterns = [
    # ... твои другие пути
    path("import-products/", ProductImportView.as_view(), name="import_products"),
]

router = DefaultRouter()
router.register(r'attributes', ProductAttributeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

path('accounts/', include('allauth.urls')),

sentry_sdk.init(
    dsn="https://YOUR_SENTRY_DSN_HERE",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)


urlpatterns = [
    ...
    path('test-error/', TestErrorView.as_view(), name='test-error'),
]
