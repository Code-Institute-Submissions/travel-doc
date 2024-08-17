from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
#from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Job, Speciality, JobApplication
from .forms import JobAddForm, JobApplicationForm
from django.db import IntegrityError


# Create your views here.
# Add Job for employers
class AddJob(LoginRequiredMixin,UserPassesTestMixin, CreateView,):
    """ Model to submit a job
    """
    model = Job
    form_class = JobAddForm
    template_name = 'jobs/add_job.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        if self.object.status == 0:
            messages.info(
                self.request, """Your Job was sent successfully <br>
    and is awaiting approval."""
                )
        return response

    def test_func(self):
        return self.request.user.profile.user_type == 'employer'

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to add a job!")
        return redirect('home')

    
# Job detail view
def job_detail_view(request, slug):
    job = get_object_or_404(Job, slug=slug)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.job = job
                application.applicant = request.user
                application.save()
                messages.success(request, "Your application has been submitted. We will reach out to you shortly!")
                return redirect('job_detail', slug=slug)
            except IntegrityError:
                messages.error(request, "You have already applied for this job.")
                return redirect('job_detail', slug=slug)
    else:
        form = JobApplicationForm()

    return render(
        request,
        'jobs/job_detail.html',
        {'job': job,
        'form': form
        }
    )


#Speciality View
class SpecialityView(ListView):
    """
    """
    template_name = 'jobs/speciality.html'
    context_object_name = 'speclist'

    def get_queryset(self):
        content = {
            'spec': self.kwargs['speciality'],
            'jobs': Job.objects.filter(speciality__name=self.kwargs[
                'speciality']).filter(status=1)
        }
        return content


def speciality_list(request):
    speciality_list = Speciality.objects.exclude(name='other')
    context = {
        'speciality_list': speciality_list
    }
    return context