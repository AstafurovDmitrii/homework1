from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

from django.urls import path, include

urlpatterns = [
    path('api/', include('shop.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),  # login/logout/password reset
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  
    path('api/auth/social/', include('allauth.socialaccount.urls')),  # соцсети
]
