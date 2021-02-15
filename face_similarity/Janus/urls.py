from django.urls import path
from . import views

app_name = 'janus'
#path('score/',views.Janus_API.as_view(),name='janus_api')
urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    path('upload/',views.FileFieldView.as_view(),name='upload'),
    path('clusters/',views.ShowClusters.as_view(),name='show_clusters'),
]
