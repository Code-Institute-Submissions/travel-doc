from django.urls import path
from . import views
from .views import *


"""url paths"""
urlpatterns = [
    path('speciality/<speciality>/', views.SpecialityView.as_view(),
          name='speciality'),
    path('job/add/', JobCreateOrUpdateView.as_view(), name='add_job'),
    path('job/edit/<int:pk>/', JobCreateOrUpdateView.as_view(), name='edit_job'),
    path('job/delete/<int:pk>/', JobDeleteView.as_view(), name='job_delete'),
    path('jobs/<slug:slug>/', views.job_detail_view, name='job_detail'),   
]