from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from . import models
from .models import Job, Speciality


@admin.register(Job)
class JobsAdmin(SummernoteModelAdmin):
    """
    Admin for Jobs model
    """
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    summernote_fields = ('job_description',)
    list_display = ('title', 'speciality', 'created_on', 'author','start_date', 'end_date','location')
    search_fields = ['speciality', 'author']
    
    
    admin.site.register(Speciality)
