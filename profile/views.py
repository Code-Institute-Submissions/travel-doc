from django.views.generic import TemplateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from allauth.account.views import LogoutView
from .models import Profile
from blog.models import Post, Comment
from .forms import ProfileForm

# Create your views here.
class ProfileView(TemplateView):
    """" profile view """
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(user=self.kwargs["pk"])
            context['profile'] = profile
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")
        
        return context


class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """edit  profile view """
    form_class = ProfileForm
    model = Profile
    template_name ='edit_profile.html'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Your progile has been updated successfully!")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('profile',kwargs={'pk': self.kwargs['pk']})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user