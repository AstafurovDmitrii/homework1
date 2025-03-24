from django.shortcuts import render
from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'  # Шаблон, который будет использоваться

    ordering = '-published_at'  # Сортируем статьи по дате (новые первыми)
    
    articles = Article.objects.all().order_by(ordering).prefetch_related('scopes')  # Загружаем статьи с тегами

    context = {'articles': articles}  # Передаем статьи в шаблон

    return render(request, template, context)
