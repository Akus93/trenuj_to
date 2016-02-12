from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.name


class Shortcut(models.Model):
    title = models.CharField(max_length=128, unique=True, verbose_name='Tytuł')
    description = models.TextField(max_length=256, verbose_name='Opis')
    category = models.ForeignKey(Category, verbose_name='Kategoria')
    image = models.ImageField('Obrazek', upload_to='shortcut_images')
    author = models.ForeignKey(User)
    link = models.URLField(verbose_name='Adres artykułu')
    is_active = models.BooleanField(default=False, verbose_name='Aktywny?')

    class Meta:
        verbose_name_plural = "Kafelki"

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=128, unique=True)
    intro = models.TextField(max_length=512)
    text = models.TextField()
    title_image = models.CharField(max_length=32, unique=True)
    images_dir = models.CharField(max_length=32, unique=True)
    author = models.ForeignKey(User)
    create_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Artykuły"

    def __str__(self):
        return self.title


class Tag(models.Model):
    shortcut = models.ForeignKey(Shortcut)
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Tagi"

    def __str__(self):
        return self.name



