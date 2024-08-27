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
from django.core.exceptions import PermissionDenied



# Add or edit Job for employers
class JobCreateOrUpdateView(LoginRequiredMixin,UserPassesTestMixin, CreateView, UpdateView):
    """ View to add or edit a job for employers
    """
    model = Job
    form_class = JobAddForm
    template_name = 'jobs/add_job.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        #Set the author to the current user
        form.instance.author = self.request.user

        #Set job´s status to published
        form.instance.status = 1

        #Check if this is an update or a new creation
        if self.get_object(): #If an object exists, It´s an update
            response = super().form_valid(form)
            messages.success(self.request, "Job updated successfully!")

            # Redirect to the employer's profile after the update
            return redirect(reverse_lazy('profile', kwargs={'pk': form.instance.author.profile.pk}))

        else: #If no object exists, it´s a new job creation
            response = super().form_valid(form)
            messages.success(
                self.request, """Your Job is posted successfully!""")
        
        return response

    def test_func(self):
        if self.request.user.profile.user_type == 'employer':
            return True
        raise PermissionDenied("You are not authorized to add a job.")


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

    # Initialize the variable to avoid UnboundLocalError
    existing_application = None
    if request.user.is_authenticated:
        existing_application = JobApplication.objects.filter(job=job, applicant=request.user).first()
    
    if not request.user.is_authenticated:
        messages.info(request, "You need an account to apply for jobs! Please Signup!")
        # Redirect to the signup page if the user is not authenticated
        return redirect('account_signup')

    if request.method == 'POST':
        if request.user.is_authenticated and request.user.profile.user_type == 'employer':
            messages.error(request, "You are not authorized to apply for jobs!")
            return redirect('job_detail', slug=job.slug)

        #If a jobapplication exists we can update it
        existing_application = JobApplication.objects.filter(job=job, applicant=request.user).first()
        form = JobApplicationForm(request.POST, request.FILES, instance=existing_application)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.speciality = job.speciality

            
            if existing_application:
             # Reset status to 'Applied' when updating an existing application   
                application.status = 0
                application.save()
                messages.success(request, "Your application has been updated and will be reviewed again.")
                return redirect('profile', pk=request.user.pk)
            else:
                # Set initial status for new applications
                application.status = 0
                application.save()
                messages.success(request, "Thank you for your application. It will be reviewed shortly.")
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