from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'', include('trenuj.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^accounts/', include('allauth.urls')),
]
