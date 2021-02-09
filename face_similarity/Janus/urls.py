from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.IndexView.as_view(),name='home'),
    #path('score/',views.Janus_API.as_view(),name='janus_api')
]
