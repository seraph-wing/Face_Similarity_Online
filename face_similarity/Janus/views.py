from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from django.urls import reverse_lazy
from PIL import Image
# Create your views here.


class IndexView(TemplateView):
    template_name = 'Janus/index.html'

class Janus_API():
    pass

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'Janus/upload.html'  # Replace with your template.
    success_url = reverse_lazy('janus:home')  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field1')
        if form.is_valid():
            for f in files:
                try:
                    im = Image.open(f)
                    im.show()  # Do something with each file.
                except e:
                    print(e.message())
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
