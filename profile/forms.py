from allauth.account.forms import SignupForm
from django import forms
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile, CustomUser


class CustomSignupForm(SignupForm):
    USER_TYPE_CHOICES = (
        ('regular','Regular User'),
        ('employer', 'Employer'),
    )

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect, required=True)

    #class Meta:
        #model = CustomUser()
        #fields = (
            #"email",
            #"username",
            #"user_type",
        #)
    

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        
        user.profile.user_type = self.cleaned_data['user_type']
        user.profile.save()
        return user


#class CustomUserChangeForm(UserChangeForm):
    #class Meta:
        #model = CustomUser()
        #fields = (
            #"email",
           # "username",
            #"user_type",
        #)


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