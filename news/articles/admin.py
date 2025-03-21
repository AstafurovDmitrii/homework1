from django.contrib import admin
from .models import Article, Tag, Scope


class ScopeInline(admin.TabularInline):
    """Позволяет редактировать разделы статьи прямо в админке."""
    model = Scope
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    inlines = [ScopeInline]  # Добавляем управление разделами в карточку статьи


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ('article', 'tag', 'is_main')
