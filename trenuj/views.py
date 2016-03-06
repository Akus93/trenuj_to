from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .services import save_tags, search_shortcuts, get_shortcuts_by_tag
from uuid import uuid4


class IndexView(generic.View):
    template_name = 'trenuj/index.html'

    def get(self, request, *args, **kwargs):
        shortcuts = Shortcut.objects.filter(is_active=True)
        return render(request, self.template_name, {'shortcuts': shortcuts})


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


class ShortcutCreateView(LoginRequiredMixin, generic.View):
    login_url = '/login/'
    template_name = 'trenuj/shortcut_create.html'
    form_class = ShortcutCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
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
    change_image_form_class = ProfileImageChangeForm

    def get(self, request, *args, **kwargs):
        change_password_form = self.form_class(request.user)
        change_image_form = self.change_image_form_class()
        user_image = None
        shortcuts = Shortcut.objects.filter(author=request.user.id)
        articles = Article.objects.filter(author=request.user.id)
        if UserImage.objects.filter(user=request.user.id).exists():
            user_image = UserImage.objects.get(user=request.user.id)
        return render(request, self.template_name, {'change_password_form': change_password_form,
                                                    'change_image_form': change_image_form,
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
        extension = request.FILES['image'].name.split('.')[-1]
        request.FILES['image'].name = '{0}.{1}'.format(uuid4(), extension)
        form = self.form_class(request.POST, request.FILES, user=request.user.id)
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




