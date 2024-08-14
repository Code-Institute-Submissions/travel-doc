from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Global Doctors"
        message = f"Hi {instance.username},\n\nThank you for signing up at Global Doctors!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        #send_mail(subject, message, from_email, recipient_list)
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.send(fail_silently=False)