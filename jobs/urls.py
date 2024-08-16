from django.urls import path
from . import views
from .views import *


"""url paths"""
urlpatterns = [
    path('speciality/<speciality>/', views.SpecialityView.as_view(),
          name='speciality'),
    path('add_job/', views.AddJob.as_view(), name='add_job'),
    path('jobs/<slug:slug>/', views.job_detail_view, name='job_detail'),   
]