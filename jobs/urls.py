from django.urls import path
from . import views
from .views import *


"""url paths"""
urlpatterns = [
    path('speciality/<str:speciality>/', SpecialityView.as_view(), name='speciality_jobs'),
    path('job/add/', JobCreateOrUpdateView.as_view(), name='add_job'),
    path('job/edit/<int:pk>/', JobCreateOrUpdateView.as_view(), name='edit_job'),
    path('job/<int:pk>/delete/', views.job_delete_view, name='job_delete'),
    path('jobs/<slug:slug>/', views.job_detail_view, name='job_detail'),
    path('jobs/<slug:slug>/edit', views.job_detail_view, name='edit_application'),
    path('job_application/<int:pk>/delete/', views.job_application_delete_view, name='delete_application'),   
]