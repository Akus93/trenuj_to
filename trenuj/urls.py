from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from trenuj_to import settings
from . import views

urlpatterns = [
       url(r'^$', views.IndexView.as_view(), name='index'),
       url(r'^signup/$', views.SignupView.as_view(), name='signup'),
       url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
       url(r'^shortcut/create/$', views.ShortcutCreateView.as_view(), name='shortcut_create'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)