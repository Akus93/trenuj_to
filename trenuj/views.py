from django.views import generic
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import *


class IndexView(generic.TemplateView):
    template_name = 'trenuj/index.html'


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
