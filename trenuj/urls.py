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

    url(r'^account/$', views.AccountView.as_view(), name='account'),
    url(r'^account/password/change/$', views.ChangePasswordView.as_view(), name='change_password'),
    url(r'^account/image/change/$', views.ChangeProfileImageView.as_view(), name='change_image'),

    url(r'^links/$', views.LinksView.as_view(), name='links'),
    url(r'^videos/$', views.VideosView.as_view(), name='videos'),
    url(r'^images/$', views.ImagesView.as_view(), name='images'),
    # url(r'^articles/$', views.ArticlesView.as_view(), name='articles'),

    url(r'^link/create/$', views.LinkCreateView.as_view(), name='link_create'),
    url(r'^video/create/$', views.VideoCreateView.as_view(), name='video_create'),
    url(r'^image/create/$', views.ImageCreateView.as_view(), name='image_create'),
    url(r'^article/create/$', views.ArticleCreateView.as_view(), name='article_create'),
    url(r'^article/view/(?P<slug>[\w-]+)/$', views.ArticleView.as_view(), name='article'),
    url(r'^article/edit/(?P<slug>[\w-]+)/$', views.ArticleUpdateView.as_view(), name='article_edit'),
    url(r'^article/delete/(?P<slug>[\w-]+)/$', views.ArticleDeleteView.as_view(), name='article_delete'),

    url(r'^user/(?P<username>[\w]+)/media/$', views.UserMediaView.as_view(), name='user_media'),
    url(r'^category/(?P<name>[\w-]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag>[\w]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^start/$', views.StartView.as_view(), name='start'),  # slajder z rejestracja
    url(r'^ajax/$', views.entry_index, name='ajax'),            # test endlesspagination
    url(r'^user/(?P<username>[\w]+)/follow/delete/$', views.FollowDeleteView.as_view(), name='delete_follow'),
    url(r'^clipboard/delete/(?P<shortcut_id>[\d]+)/$', views.ClipboardDeleteView.as_view(), name='delete_clipboard'),

    # API
    url(r'^api/follow/$', views.AddFollowerView.as_view(), name='follow'),
    url(r'^api/clipboard/add/$', views.AddToClipboardView.as_view(), name='add_to_clipboard'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
