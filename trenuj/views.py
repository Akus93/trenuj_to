from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

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
        form = self.form_class(request.POST, request.FILES, author=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})

