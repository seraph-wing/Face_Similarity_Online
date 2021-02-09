from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class IndexView(TemplateView):
    template_name = 'Janus/index.html'

class Janus_API():
    pass
