
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import os

def home_view(request):
    return render(request, 'app/home.html', {
        'pages': {
            'Домашняя страница': '/',
            'Текущее время': '/current_time/',
            'Содержимое рабочей директории': '/workdir/',
        }
    })

def current_time_view(request):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return HttpResponse(f"Текущее время: {now}")

def workdir_view(request):
    files = os.listdir('.')
    return HttpResponse(f"Содержимое рабочей директории:<br>{'<br>'.join(files)}")
