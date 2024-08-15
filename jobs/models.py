from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.core.validators import MinValueValidator, MaxValueValidator


STATUS = ((0, "Draft"), (1, "Published"))
CustomUser = get_user_model()


# Create your models here.
class Speciality(models.Model):
    """
    Model for Speciality
    Stores multiple job post entries related to :model:`jobs`
    and :model:`job.Speciality`
    """
    class Meta:
        verbose_name_plural = 'Specialities'
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    """
    Model to store jobs
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
    CustomUser, on_delete=models.CASCADE, related_name="job_posts")
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT, default=4)
    location = models.CharField(max_length=100, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    updated_on = models.DateTimeField(auto_now=True)
    stars = models.PositiveIntegerField(
        default=3,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)]
    )
    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title