from django.views import generic
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .services import save_tags, search_shortcuts, get_shortcuts_by_tag
from base64 import b64decode
from .models import Slider


class IndexView(generic.View):
    template_name = 'trenuj/index.html'

    def get(self, request, *args, **kwargs):
        shortcuts = Shortcut.objects.filter(is_active=True)
        slider = Slider.objects.filter(is_active=True)[:3]
        return render(request, self.template_name, {'shortcuts': shortcuts, 'slider': slider})


class LoginView(generic.View):
    pass


class LogoutView(generic.View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class SignupView(generic.TemplateView):
    form_class = SignupForm
    template_name = 'trenuj/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class LinkCreateView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    template_name = 'trenuj/link_create.html'
    form_class = LinkCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.FILES.get('image'):
            extension = request.FILES['image'].name.split('.')[-1]
            request.FILES['image'].name = '{0}.{1}'.format(uuid4(), extension)
        tags = request.POST.get('tags', '')
        form = self.form_class(request.POST, request.FILES, author=request.user.id)
        if form.is_valid():
            shortcut = form.save()
            if tags:
                save_tags(shortcut.id, tags)
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class ImageCreateView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    template_name = 'trenuj/image_create.html'
    form_class = ImageCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.FILES.get('image'):
            extension = request.FILES['image'].name.split('.')[-1]
            request.FILES['image'].name = '{0}.{1}'.format(uuid4(), extension)
        tags = request.POST.get('tags', '')
        form = self.form_class(request.POST, request.FILES, author=request.user.id)
        if form.is_valid():
            shortcut = form.save()
            if tags:
                save_tags(shortcut.id, tags)
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class AccountView(LoginRequiredMixin, generic.View):
    login_url = '/login'
    template_name = 'trenuj/account.html'
    form_class = ChangePasswordForm
    # change_image_form_class = ProfileImageChangeForm

    def get(self, request, *args, **kwargs):
        change_password_form = self.form_class(request.user)
        # change_image_form = self.change_image_form_class()
        user_image = None
        shortcuts = Shortcut.objects.filter(author=request.user.id).order_by('-create_date')
        articles = Article.objects.filter(author=request.user.id).order_by('-create_date')
        if UserImage.objects.filter(user=request.user.id).exists():
            user_image = UserImage.objects.get(user=request.user.id)
        return render(request, self.template_name, {'change_password_form': change_password_form,
                                                    'user_image': user_image,
                                                    'articles': articles,
                                                    'shortcuts': shortcuts})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account/')
        return render(request, self.template_name, {'form': form})


class ChangePasswordView(LoginRequiredMixin, generic.View):
    login_url = '/login'
    form_class = ChangePasswordForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
        return render(request, 'trenuj/account.html', {'change_password_form': form, 'error_change_password': True})


class ChangeProfileImageView(LoginRequiredMixin, generic.View):
    login_url = '/login'
    form_class = ProfileImageChangeForm

    def post(self, request, *args, **kwargs):
        img64 = request.POST['imagebase64'].split(',')[1]
        circle_image = b64decode(img64)
        form = self.form_class(request.POST, request.FILES, user=request.user.id, circle_image=circle_image)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/account/')


class ArticleCreateView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    form_class = ArticeCreateForm
    template_name = 'trenuj/article_create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, user=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account/')
        return render(request, 'trenuj/account.html', {'form': form})


class ArticleView(generic.DetailView):
    model = Article
    template_name = 'trenuj/article.html'
    context_object_name = 'article'


class CategoryView(generic.View):
    template_name = 'trenuj/category.html'

    def get(self, request, *args, **kwargs):
        category_name = self.kwargs['name']
        category_shortcuts = Shortcut.objects.filter(category__name=category_name, is_active=True)
        return render(request, self.template_name, {'shortcuts': category_shortcuts})


class SearchView(generic.View):
    template_name = 'trenuj/search.html'

    def post(self, request, *args, **kwargs):
        words = request.POST['search']
        results = search_shortcuts(words)
        return render(request, self.template_name, {'results': results})


class TagView(generic.View):
    template_name = 'trenuj/tag.html'

    def get(self, request, *args, **kwargs):
        tag = self.kwargs['tag']
        results = get_shortcuts_by_tag(tag)
        return render(request, self.template_name, {'results': results})


class StartView(generic.TemplateView):
    template_name = 'trenuj/start.html'


from el_pagination.decorators import page_template
@page_template('trenuj/entry_index_page.html')
def entry_index(
        request, template='trenuj/entry_index.html', extra_context=None):
    context = {
        'entries': Shortcut.objects.all(),
    }
    if extra_context is not None:
        context.update(extra_context)
    from django.template import RequestContext
    return render_to_response(
        template, context, context_instance=RequestContext(request))


class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    model = Article
    fields = ['title', 'content']
    template_name = 'trenuj/article_edit.html'
    context_object_name = 'form'
    success_url = '/account#articles'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseRedirect('/')
        return super(ArticleUpdateView, self).dispatch(request, *args, **kwargs)


class ArticleDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = '/login/'
    model = Article
    success_url = '/account#articles'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return HttpResponseRedirect('/')
        return super(ArticleDeleteView, self).dispatch(request, *args, **kwargs)


class VideoCreateView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    template_name = 'trenuj/video_create.html'
    form_class = VideoCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        tags = request.POST.get('tags', '')
        form = self.form_class(request.POST, author=request.user.id)
        if form.is_valid():
            video = form.save()
            if tags:
                save_tags(video.id, tags)
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class UserMediaView(generic.View):
    template_name = 'trenuj/user_media.html'

    def get(self, request, *args, **kwargs):
        user = self.kwargs['username']
        shortcuts = Shortcut.objects.filter(author__username=user, is_active=True)
        return render(request, self.template_name, {'shortcuts': shortcuts})


