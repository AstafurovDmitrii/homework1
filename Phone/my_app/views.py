from django.shortcuts import render, get_object_or_404
from phones.models import Phone

def show_catalog(request):
    sort_param = request.GET.get('sort')  # Получаем параметр сортировки
    phones = Phone.objects.all()

    if sort_param == 'name':
        phones = phones.order_by('name')
    elif sort_param == 'price_asc':
        phones = phones.order_by('price')
    elif sort_param == 'price_desc':
        phones = phones.order_by('-price')

    return render(request, 'catalog.html', {'phones': phones})

def show_phone(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    return render(request, 'phone_detail.html', {'phone': phone})
