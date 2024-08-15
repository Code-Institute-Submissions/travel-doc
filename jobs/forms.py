from django import forms
from .models import Job
from slugify import slugify
from django_summernote.widgets import SummernoteWidget


class JobForm(forms.ModelForm):
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
