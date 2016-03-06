from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from trenuj_to import settings
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^shortcut/create/$', views.ShortcutCreateView.as_view(), name='shortcut_create'),
    url(r'^account/$', views.AccountView.as_view(), name='account'),
    url(r'^account/password/change/$', views.ChangePasswordView.as_view(), name='change_password'),
    url(r'^account/image/change/$', views.ChangeProfileImageView.as_view(), name='change_image'),
    url(r'^article/create/$', views.ArticleCreateView.as_view(), name='article_create'),
    url(r'^article/view/(?P<slug>[\w-]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^category/(?P<name>[\w-]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
