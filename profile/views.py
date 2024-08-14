from django.views.generic import TemplateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from allauth.account.views import LogoutView
from .models import Profile
from blog.models import Post, Comment
from .forms import ProfileForm, CustomUserChangeForm, CustomUserCreationForm

# Create your views here.
class ProfileView(TemplateView):
    """" profile view """
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.kwargs["pk"])
        context['profile'] = profile
        
        return context


class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """edit  profile view """
    form_class = ProfileForm
    model = Profile

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('profile',kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        return self.request.user == self.get_object().user