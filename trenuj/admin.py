from django.contrib import admin
from .models import *


admin.site.register([Shortcut, Article, Category, Tag])
