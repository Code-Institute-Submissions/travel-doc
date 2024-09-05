from django.views.generic import UpdateView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from allauth.account.views import SignupView
from .models import Profile, CustomUser
from .forms import RegularProfileForm, EmployerProfileForm
from blog.models import Post
from jobs.models import Job, JobApplication


class CustomSignupView(SignupView):
    def form_valid(self, form):
        response = super().form_valid(form)

        return response

    def get_success_url(self):
        if self.user and self.user.pk:
            return reverse('profile', args=[self.user.pk])
        else:
            return reverse('account_signup')


@login_required
def regular_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    posts = Post.objects.filter(author=request.user).order_by('-created_on')
    job_applications = JobApplication.objects.filter(applicant=request.user)

    context = {
        'profile': profile,
        'posts': posts,
        'job_applications': job_applications,
    }
    return render(request, 'profile/regular_profile.html', context)


@login_required
def employer_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    posts = Post.objects.filter(author=request.user).order_by('-created_on')
    jobs = Job.objects.filter(author=request.user)

    context = {
        'profile': profile,
        'posts': posts,
        'jobs': jobs,
    }
    return render(request, 'profile/employer_profile.html', context)


@login_required
def profile_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if profile.user_type == 'employer':
        return redirect('employer_profile', pk=pk)
    else:
        return redirect('regular_profile', pk=pk)


class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """edit  profile view that handles both regular and employer profiles
    """
    template_name = 'profile/edit_profile.html'

    def get_form_class(self):
        profile = self.get_object()
        if profile.user_type == 'employer':
            return EmployerProfileForm
        else:
            return RegularProfileForm

    def form_valid(self, form):
        self.object = form.save()
        messages.success(
            self.request,
            "Your profile has been updated successfully!")
        if form.is_valid():
            profile = form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        profile = self.object

        if profile.user_type == 'employer':
            return reverse_lazy('employer_profile', kwargs={'pk': profile.pk})
        else:
            return reverse_lazy('regular_profile', kwargs={'pk': profile.pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
