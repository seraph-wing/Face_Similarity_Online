from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from django.urls import reverse_lazy
from PIL import Image
from datetime import datetime
import os
from . import preprocessing
# Create your views here.

def save_to_sys(files,k,path):
    """
    utility function to save posted files to system for processing by ML code
    files: request.files list
    k: id of cluster
    path: path to be saved to
    """
    for (i,f) in enumerate(files):
        try:
            #print(f)
            im = Image.open(f)
            #print(path + '/cluster1_'+str(i)+'.jpg')
            im.save(path + '/cluster_'+str(k)+'_'+str(i)+'.jpg')  # Do something with each file.
            im.close()
        except Exception as e:
            print(e)
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
        files1 = request.FILES.getlist('file_field1')
        files2 = request.FILES.getlist('file_field2')
        now = datetime.now()
        path = 'D:/Public projects/ML web apps/Face similarity/Face_Similarity_Online/face_similarity/media/' + now.strftime("%d_%m_%Y_%H_%M_%S")
        os.mkdir(path)
        if form.is_valid():
            #saving files to system for processing(PRE-PROCESSING STEPS)
            save_to_sys(files1,1,path)
            save_to_sys(files2,2,path)
            #PROCESSING, TO BE PROCESSED BY THE ml CODE AND CLUSTERS MADE
            face_lists = preprocessing.get_face_list(path)
            dataset = preprocessing.create_dataset(face_lists)
            clustered_faces = preprocessing.get_clustered_faces(dataset)
            #SEND THE RESPECTIVE CLUSTERS BACK FOR USERS TO CHOOSE

            #GET CHOICES AND FIND SIMILARITY BETWEEN THEM
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
