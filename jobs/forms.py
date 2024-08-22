from django import forms
from .models import Job, JobApplication
from slugify import slugify
from django_summernote.widgets import SummernoteWidget


class JobAddForm(forms.ModelForm):
    """
    Form for Jobsubmission
    """
    title = forms.CharField(max_length=200)

    def save(self, commit=True):
        instance = super().save(commit=False)
        #Set the slug value from the title
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Job
        fields = ['title', 'speciality', 'location', 'start_date', 'end_date', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'speciality': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'placeholder': '01.12.2024'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'placeholder': '31.12.2024'}),
            'description': SummernoteWidget(attrs={'class': 'form-control'}),
        }

        labels = {
            "title": "Job Title",
            "speciality": "Speciality",
            "location": "Location",
            "start_date": "Start Date",
            "end_date": "End Date",
            "description": "Job Description",
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'applicant_first_name', 
            'applicant_last_name', 
            'applicant_email', 
            'applicant_phone',  
            'message', 
            'cv']
        widgets = {
            'message' : forms.Textarea(attrs={'rows':4}),
        }

        labels = {
            'applicant_first_name': "Enter first name", 
            'applicant_last_name': "Enter last name",
            'applicant_email': "Email address", 
            'applicant_phone': "Phone number", 
            'message':"Message", 
            'cv': "UPLOAD CV/RESUME(optional)",
        }
        
    def __init__(self, *args, **kwargs):
        self.job = kwargs.pop('job', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.job:
            self.fields['cv'].required =False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.job = self.job
            instance.applicant = self.user
            instance.save()
        return instance