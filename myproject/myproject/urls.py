"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from app import views  # Импортируем view-функции из приложения

urlpatterns = [
    path('admin/', admin.site.urls),  # Панель администратора
    path('', views.home_view, name='home'),  # Главная страница
    path('current_time/', views.current_time_view, name='current_time'),  # Текущее время
    path('workdir/', views.workdir_view, name='workdir'),  # Содержимое рабочей директории
]
