from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Profile, CustomUser


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'user_type',
        'display_name',
        'profile_image',
    )


admin.site.register(CustomUser)
admin.site.register(Profile, ProfileAdmin)
