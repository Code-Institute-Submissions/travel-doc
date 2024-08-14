from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class ProfileForm(forms.ModelForm):
    """ form for user to create a profile"""
    class Meta:
        model = Profile
        fields = ['profile_image', 'display_name', 'bio']

        labels = {
            "profile_image": "Profile Image",
            "display_name": "Display Name",
            "bio": "Bio"
        }