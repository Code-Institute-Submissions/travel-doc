# Generated by Django 4.2.14 on 2024-08-16 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='applicant_email',
            field=models.EmailField(default=0, max_length=254),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='applicant_first_name',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='applicant_last_name',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='applicant_phone',
            field=models.CharField(default=0, max_length=20),
        ),
    ]