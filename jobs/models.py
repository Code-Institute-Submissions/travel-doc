from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField


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
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(
    CustomUser, on_delete=models.CASCADE, related_name="job_posts")
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)
    location = models.CharField(max_length=100)
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


APPLICATION_STATUS = (
    (0, "Applied"),
    (1, "Sent to Employer"),
    (2, "Accepted"),
    (3, "Rejected"),
)

class JobApplication(models.Model):
    """job application"""
    job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="applications")
    applicant_first_name = models.CharField(max_length=100)
    applicant_last_name = models.CharField(max_length=100)
    applicant_email = models.EmailField()
    applicant_phone = models.CharField(max_length=20)
    message = models.TextField(null=True, blank=True)
    cv = CloudinaryField('file', blank=True)
    status = models.IntegerField(choices=APPLICATION_STATUS, default=0)
    applied_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-applied_on"]
        unique_together = ("job", "applicant")

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"


class JobRating(models.Model):
    """job star rating
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("job", "user")

    def __str__(self):
        return f'{self.user} rated {self.job.title} with {self.rating} stars'
