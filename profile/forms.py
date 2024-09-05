from allauth.account.forms import SignupForm
from django import forms
from .models import Profile, CustomUser
from cloudinary.forms import CloudinaryInput


class CustomSignupForm(SignupForm):
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User'),
        ('employer', 'Employer'),
    )

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.profile.user_type = self.cleaned_data['user_type']
        user.profile.save()
        return user


class RegularProfileForm(forms.ModelForm):
    """ form for regular user profile"""
    class Meta:
        model = Profile
        fields = ['profile_image', 'display_name', 'bio']

        widgets = {
            'profile_image': forms.ClearableFileInput(
                attrs={'class': 'form-control'}),
        }

        labels = {
            "profile_image": "Profile Image",
            "display_name": "Display Name",
            "bio": "Bio"
        }


class EmployerProfileForm(forms.ModelForm):
    """Form for employer user profile"""
    class Meta:
        model = Profile
        fields = ['profile_image', 'display_name', 'bio']

        widgets = {
            'profile_image': forms.ClearableFileInput(
                attrs={'class': 'form-control'}),
        }

        labels = {
            "profile_image": "Profile Image",
            "display_name": "Display Name",
            "bio": "Bio"
        }
