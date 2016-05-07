from django.contrib import admin
from .models import *


class ShortcutAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_active', 'create_date', 'type')
    list_filter = ['create_date', 'is_active']
    search_fields = ['title', 'author__username']
    list_editable = ['is_active']
    list_per_page = 25


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'create_date')
    list_filter = ['create_date']
    search_fields = ['title']
    list_per_page = 25


admin.site.register(Shortcut, ShortcutAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register([Category, Tag, UserImage, Slider])
