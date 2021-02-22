from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views import View
from .forms import FileFieldForm,ShowClusersForm
from django.urls import reverse_lazy
from PIL import Image
from datetime import datetime
import os
from . import preprocessing
import shutil
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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
    success_url = reverse_lazy('janus:show_clusters')  # Replace with your URL or reverse().

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


class ShowClusters(FormView,SuccessMessageMixin):
    form_class = ShowClusersForm
    template_name = 'Janus/show_clusters.html'
    success_url = reverse_lazy('janus:score')
    #success_message = 'hellow there!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        path = 'D:/Public projects/ML web apps/Face similarity/Face_Similarity_Online/face_similarity/media/montage'
        #os.mkdir(path)
        clusters = []
        for montage in os.listdir(path):
            if montage.endswith('.jpg'):
                clusters.append('montage/'+montage)
        context['clusters'] = clusters
        #print(self.request.POST.get('cluster1'))
        return context

    def post(self,*args,**kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        clus1 = self.request.POST.get('cluster_1')
        clus2 = self.request.POST.get('cluster_2')
        path = 'D:/Public projects/ML web apps/Face similarity/Face_Similarity_Online/face_similarity/media/montage'
        if form.is_valid():
            #FIND SCORE BASED ON CLUSTERS
            print(int(clus1))
            print(int(clus2))
            score = preprocessing.get_similarity_score(int(clus1),int(clus2))
            print(score*100)
            messages.add_message(self.request, messages.INFO, str(score*100))
            shutil.rmtree(path)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
class ShowScore(TemplateView):
    template_name = 'Janus/show_score.html'
