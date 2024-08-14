from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings 
#from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


#CustomUser = get_user_model()

# Create your models here.
class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set', blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name= 'customuser_set', blank=True,
    )
    pass


class Profile(models.Model):
    """Profile model """
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User'),
        ('employer', 'Employer'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='regular')
    profile_image = CloudinaryField('image', default='placeholder', blank=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
