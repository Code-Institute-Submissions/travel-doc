from django.urls import path
from . import views
from .views import *


"""url paths"""
urlpatterns = [
    path('speciality/<speciality>/', views.SpecialityView.as_view(),
          name='speciality'),
    path('job/add/', JobCreateOrUpdateView.as_view(), name='add_job'),
    path('job/edit/<int:pk>/', JobCreateOrUpdateView.as_view(), name='edit_job'),
    path('job/<int:pk>/delete/', views.job_delete_view, name='job_delete'),
    path('jobs/<slug:slug>/', views.job_detail_view, name='job_detail'),
    path('job/<int:pk>/edit_application', views.job_detail_view, name='edit_application'),
    path('job_application/<int:pk>/delete/', views.job_application_delete_view, name='delete_application'),   
]