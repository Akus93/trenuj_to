from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.name


class Shortcut(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=256)
    category = models.ForeignKey(Category)
    image = models.CharField(max_length=32, unique=True)
    author = models.ForeignKey(User)
    link = models.URLField()
    is_active = models.BooleanField(default=False)
    entrance = models.IntegerField(default=0)

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



