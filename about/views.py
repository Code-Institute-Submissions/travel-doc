from django.shortcuts import render, redirect
from .models import About
from django.contrib import messages
from .forms import ContactForm


def about_me(request):
    """
    Renders the About page
    """
    about = About.objects.all().order_by('-updated_on').first()

    return render(
        request,
        "about/gmdhome.html",
        {"about": about},
    )

def contact(request):
    """
    Renders the contact page
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been sent successfully!")

            return redirect('home')
        else:
            messages.error(request, "There was an error with your submission. Please try again.")
    else:
        form = ContactForm()
    
    return render(
        request, 
        "about/contact.html",{
            'form': form
        }
    )