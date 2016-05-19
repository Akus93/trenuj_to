from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'', include('trenuj.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^redactor/', include('redactor.urls')),
    url('', include('social.apps.django_app.urls', namespace='social'))
]
