from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-имя")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('games:category_detail', kwargs={'category_slug': self.slug})

class Game(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='games', verbose_name="Категория")
    title = models.CharField(max_length=200, verbose_name="Название игры")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL-имя")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image_url = models.URLField(blank=True, verbose_name="Ссылка на обложку")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('games:game_detail', kwargs={'game_slug': self.slug})
