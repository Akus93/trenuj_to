from django.conf.urls import url
from . import views

urlpatterns = [
       url(r'^$', views.IndexView.as_view(), name='index'),
       url(r'^signup/$', views.SignupView.as_view(), name='signup'),
       url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
]
