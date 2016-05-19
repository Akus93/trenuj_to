from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from redactor.fields import RedactorField
from bs4 import BeautifulSoup
from os import remove as remove_file, path
from trenuj_to import settings
from embed_video.fields import EmbedVideoField


class Category(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Kategorie"
        verbose_name = 'kategoria'

    def __str__(self):
        return self.name


class Shortcut(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name='Tytuł')
    description = models.TextField(max_length=256, verbose_name='Opis', blank=True)
    category = models.ForeignKey(Category, verbose_name='Kategoria')
    image = models.ImageField('Obrazek', upload_to='shortcut_images', blank=True)
    author = models.ForeignKey(User, verbose_name='Autor')
    link = models.URLField(verbose_name='Adres artykułu', blank=True)
    video = EmbedVideoField(verbose_name='Adres do filmu', blank=True)
    type = models.CharField(verbose_name='Typ', max_length=10)
    is_active = models.BooleanField(default=False, verbose_name='Aktywny?')
    create_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Data dodania')

    class Meta:
        verbose_name_plural = "Kafelki"
        verbose_name = 'kafelek'
        ordering = ['-create_date']

    def __str__(self):
        return self.title


@receiver(pre_delete, sender=Shortcut)
def shortcut_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)


class Slider(models.Model):
    title = models.CharField(max_length=64, verbose_name='Tytuł')
    description = models.TextField(max_length=256, verbose_name='Opis')
    link = models.URLField(verbose_name='Adres artykułu', blank=True)
    image = models.ImageField('Obrazek', upload_to='slider_images', blank=True)
    is_active = models.BooleanField(default=False, verbose_name='Aktywny?')
    create_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Data dodania')

    class Meta:
        verbose_name_plural = "Slider"
        verbose_name = 'slide'
        ordering = ['-create_date']

    def __str__(self):
        return self.title


@receiver(pre_delete, sender=Slider)
def slider_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class Article(models.Model):
    title = models.CharField(max_length=128, unique=True, verbose_name='Tytuł')
    slug = models.SlugField()
    content = RedactorField(verbose_name='Artykuł',
                            redactor_options={'lang': 'pl', 'formatting': ['p', 'blockquote', 'h5'],
                                              'buttons': ['formatting', 'bold', 'italic', 'deleted', 'image', 'video',
                                                          'link', 'align', 'horizontalrule', 'align'],
                                              'toolbarFixed': True, 'toolbarOverflow': True})
    author = models.ForeignKey(User, verbose_name='Autor')
    create_date = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Data utworzenia')

    class Meta:
        verbose_name_plural = "Artykuły"
        verbose_name = 'artykuł'

    def __str__(self):
        return self.title


@receiver(pre_delete, sender=Article)
def article_delete(sender, instance, **kwargs):
    images = BeautifulSoup(instance.content, "html.parser").findAll('img')
    for image in images:
        img = image.attrs['src'].split('/')[-1]
        remove_file(path.join(settings.MEDIA_ROOT, 'articles/{}'.format(img)))


class Tag(models.Model):
    shortcut = models.ForeignKey(Shortcut, verbose_name='Kafelek')
    name = models.CharField(max_length=32, verbose_name='Nazwa')

    class Meta:
        verbose_name_plural = "Tagi"
        verbose_name = 'tag'

    def __str__(self):
        return '{} <- {}'.format(self.shortcut, self.name)


class UserImage(models.Model):
    user = models.OneToOneField(User, verbose_name='Użytkownik')
    image = models.ImageField('Zdjęcie profilowe', upload_to='profile_images')

    class Meta:
        verbose_name_plural = "Zdjęcia profilowe"
        verbose_name = 'zdjęcie profilowe'

    def __str__(self):
        return 'Profilowe {}'.format(self.user.get_full_name() or self.user.username)


@receiver(pre_delete, sender=UserImage)
def user_image_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', verbose_name='Użytkownik')
    follower = models.ForeignKey(User, related_name='follower')

    class Meta:
        verbose_name_plural = "Obserwowani"
        verbose_name = 'obserwowanych'

    def __str__(self):
        return '{} obserwuje {}'.format(self.follower.get_full_name() or self.follower.username,
                                        self.user.get_full_name() or self.user.username)


class Clipboard(models.Model):
    user = models.ForeignKey(User, verbose_name='Użytkownik')
    shortcut = models.ForeignKey(Shortcut, verbose_name='Kafelek')

    class Meta:
        verbose_name_plural = "Do przeczytania"
        verbose_name = 'do przeczytania'

    def __str__(self):
        return '{} chce przeczytać {}'.format(self.user.get_full_name() or self.user.username, self.shortcut.title)
