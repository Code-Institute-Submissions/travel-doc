from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
#from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Job, Speciality, JobApplication
from .forms import JobAddForm, JobApplicationForm
#from django.db import IntegrityError



# Add or edit Job for employers
class JobCreateOrUpdateView(LoginRequiredMixin,UserPassesTestMixin, CreateView, UpdateView):
    """ View to add or edit a job for employers
    """
    model = Job
    form_class = JobAddForm
    template_name = 'jobs/add_job.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        #Check if this is an update or a new creation
        if self.get_object(): #If an object exists, It´s an update
            form.instance.author = self.request.user
            response = super().form_valid(form)
            messages.success(self.request, "Job updated successfully!")

            # Redirect to the employer's profile after the update
            return redirect(reverse_lazy('profile', kwargs={'pk': form.instance.author.profile.pk}))

        else: #If no object exists, it´s a new job creation
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

    def get_object(self, get_queryset=None):
        job_id = self.kwargs.get('pk')
        if job_id:
            return Job.objects.get(pk=job_id)
        return None


#Job delete view for employer
def job_delete_view(request, pk):
    """ View to delete a job by employer
    """
    # Fetch the job using the primary key(pk)
    job = get_object_or_404(Job, pk=pk, author=request.user)

    #check if the current user is the author of the job posting
    if job.author == request.user:
        job.delete()
        messages.success(request, "Job deleted successfully!")
    else:
        messages.error(request, "You can only delete your own job")

    return redirect('profile', pk=request.user.pk)

    
# Job detail view
def job_detail_view(request, slug):
    job = get_object_or_404(Job, slug=slug)
    existing_application = JobApplication.objects.filter(job=job, applicant=request.user).first()

    if request.method == 'POST':
        if request.user.is_authenticated and request.user.profile.user_type == 'employer':
            messages.error(request, "You are not authorized to apply for jobs!")
            return redirect('job_detail', slug=job.slug)

        #If a jobapplication exists we can update it
        form = JobApplicationForm(request.POST, request.FILES, instance=existing_application)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.speciality = job.speciality
            application.save()
            if existing_application:
                messages.success(request, "Your application has been updated.")

                return redirect('profile', pk=request.user.pk)
            else:
                messages.success(request, "Your application has been submitted. We will reach out to you shortly!")

            # Redirect back to the speciality view with the list of jobs    
    
            return redirect('speciality_jobs', speciality=job.speciality.name)
            
    else:
        form = JobApplicationForm(instance=existing_application)

    return render(
        request,
        'jobs/job_detail.html',
        {'job': job,
        'form': form,
        'is_editing': bool(existing_application),
        }
    )



def job_application_delete_view(request, pk):
    """
    View to delete a job application.
    """
    application = get_object_or_404(JobApplication, pk=pk, applicant=request.user)
   
    if application.applicant == request.user:
        application.delete()
        messages.success(request, "Your job application has been deleted!")
    else:
        messages.error(request, "You can only delete your own job application.")

    # Redirect to the user´s profile using the pk
    return redirect ('profile', pk=request.user.pk)        
   

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