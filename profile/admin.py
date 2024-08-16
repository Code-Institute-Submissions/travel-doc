from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Profile, CustomUser

#from .forms import CustomUserSignupForm, ProfileForm


# Register your models here.

#class CustomUserAdmin(UserAdmin):
   # add_form = CustomUserCreationForm
    #form = CustomUserChangeForm
    #model = CustomUser
    #list_display = [
        #"email",
        #"username",
        #"is_superuser",
   # ]


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'user_type',
        'display_name',
    )


admin.site.register(CustomUser)
admin.site.register(Profile, ProfileAdmin)