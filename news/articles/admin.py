from django.contrib import admin
from .models import Article, Tag, Scope


class ScopeInline(admin.TabularInline):  # Позволяет редактировать теги внутри статьи
    model = Scope
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]  # Добавляем inline-редактирование тегов
    list_display = ('title', 'published_at')  # Добавляем отображение в списке статей
    ordering = ('-published_at',)  # Сортируем по дате публикации

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ScopeAdmin(admin.ModelAdmin):
    list_display = ('article', 'tag', 'is_main')
    list_filter = ('is_main',)  # Фильтр по основным тегам

admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Scope, ScopeAdmin)
