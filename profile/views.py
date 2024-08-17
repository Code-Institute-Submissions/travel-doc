from django.views.generic import UpdateView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
#from allauth.account.views import LogoutView
from .models import Profile
from .forms import ProfileForm
from blog.models import Post
from jobs.models import Job, JobApplication

# Create your views here.
@login_required
def regular_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    posts = Post.objects.filter(author=request.user).order_by('-created_on')
    job_application = JobApplication.objects.filter(applicant=request.user)

    context = {
        'profile':profile,
        'posts':posts,
        'job_application': job_application,
    }
    return render(request, 'profile/regular_profile.html', context)


@login_required
def employer_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    posts = Post.objects.filter(author=request.user).order_by('-created_on')
    jobs = Job.objects.filter(author=request.user)

    context = {
        'profile':profile,
        'posts': posts,
        'jobs':jobs,
    }
    return render(request, 'profile/employer_profile.html', context)


@login_required
def profile_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if profile.user_type == 'employer':
        return redirect ('employer_profile')
    else: 
        return redirect('regular_profile.html', pk=pk)


"""class ProfileView(TemplateView):
     profile view 
    template_name = 'profile/regular_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(user=self.kwargs["pk"])
            context['regular_profile'] = profile
        except Profile.DoesNotExist:
            raise Http404("Profile does not exist")
        
        return context"""


class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """edit  profile view """
    form_class = ProfileForm
    model = Profile
    template_name ='edit_profile.html'

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Your profile has been updated successfully!")
        return redirect(self.get_success_url())

    def get_success_url(self):
        profile = self.get_object()
        if profile.user_type == 'employer':
            return reverse_lazy('employer_profile')
        else:
            return reverse_lazy('regular_profile',kwargs={'pk': profile.pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user