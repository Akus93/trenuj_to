from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'home/', views.IndexView.as_view(), name='index'),
]
