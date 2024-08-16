from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . import models
from .models import Job, JobApplication, Speciality


@admin.register(Job)
class JobsAdmin(SummernoteModelAdmin):
    """
    Admin for Jobs model
    """
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    summernote_fields = ('job_description',)
    list_display = ('title', 'speciality', 'status', 'created_on', 'author','start_date', 'end_date','location')
    search_fields = ['speciality', 'author']
    

    @admin.register(JobApplication)
    class JobApplicationAdmin(admin.ModelAdmin):
        list_display = ('job', 'applicant', 'status', 'applied_on')
        search_fields = ('job_title', 'applicant__username')
        list_filter = ('status', 'applied_on')


    admin.site.register(Speciality)
