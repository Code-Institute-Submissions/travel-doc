from .models import Comment, Post
from django import forms
from django_summernote.widgets import SummernoteWidget
from cloudinary.forms import CloudinaryInput

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'featured_image','content')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'featured_image': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'content': SummernoteWidget(attrs={'class': 'form-control'}),
        }

