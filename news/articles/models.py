from django.db import models

class Tag(models.Model):
    """Модель для тематических разделов (тегов)."""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Модель для статей."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, through='Scope', related_name='articles')

    def __str__(self):
        return self.title

    def sorted_scopes(self):
        """Возвращает разделы статьи: сначала основной, потом остальные в алфавитном порядке."""
        scopes = self.scopes.all().order_by('-is_main', 'tag__name')
        return scopes


class Scope(models.Model):
    """Промежуточная таблица для связи статей и разделов."""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False)

    class Meta:
        unique_together = ('article', 'tag')  # Запрещает дублирование связок статьи и раздела

    def save(self, *args, **kwargs):
        """Проверяем, что у статьи есть только один основной раздел."""
        if self.is_main:
            Scope.objects.filter(article=self.article, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.article.title} - {self.tag.name} ({'Основной' if self.is_main else 'Дополнительный'})"
