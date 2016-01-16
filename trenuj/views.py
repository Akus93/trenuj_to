from django.views import generic


class IndexView(generic.TemplateView):
    template_name = 'trenuj/index.html'

    a = 1
    b = 2
    c = 3
