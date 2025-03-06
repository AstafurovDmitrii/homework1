from django.urls import path
from phones.views import show_catalog, show_phone

urlpatterns = [
    path('catalog/', show_catalog, name='catalog'),
    path('catalog/<slug:slug>/', show_phone, name='phone_detail'),
]
