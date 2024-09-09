from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Job, Speciality, JobApplication
from .forms import JobAddForm, JobApplicationForm, JobRatingForm
from django.core.exceptions import PermissionDenied


# Add or edit Job for employers
class JobCreateOrUpdateView(
        LoginRequiredMixin, UserPassesTestMixin, CreateView, UpdateView):
    model = Job
    form_class = JobAddForm
    template_name = 'jobs/add_job.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Set the author to the current user
        form.instance.author = self.request.user

        # Set job´s status to published
        form.instance.status = 1

        # Check if this is an update or a new creation
        if self.get_object():
            response = super().form_valid(form)
            messages.success(self.request, "Job updated successfully!")

            # Redirect to the employer's profile after the update
            return redirect(reverse_lazy(
                'profile', kwargs={'pk': form.instance.author.profile.pk}))

        else:  # If no object exists, it´s a new job creation
            response = super().form_valid(form)
            messages.success(
                self.request, """Job posted successfully!""")

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


# Job delete view for employer
def job_delete_view(request, pk):
    """ View to delete a job by employer
    """
    # Fetch the job using the primary key(pk)
    job = get_object_or_404(Job, pk=pk, author=request.user)

    # check if the current user is the author of the job posting
    if job.author == request.user:
        job.delete()
        messages.success(request, "Job deleted successfully!")
    else:
        messages.error(request, "You can only delete your own job")

    return redirect('profile', pk=request.user.pk)


# Job detail view
def job_detail_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    star_range = range(1, 6)
    half_star = job.stars % 1 != 0  # To check if there should be a half star

    # If the user is authenticated, check for existing application
    existing_application = None
    if request.user.is_authenticated:
        existing_application = JobApplication.objects.filter(
            job=job, applicant=request.user).first()

    # If the form is submitted
    if request.method == 'POST':
      
        if not request.user.is_authenticated:
            # Redirect to the Registration if the user is not authenticated
            messages.info(
                request,
            "You need an account to apply for jobs! Please Register!"
            )
        
            return redirect('account_signup')

        # Process the form for authenticated users
        if existing_application:
            form = JobApplicationForm(
                    request.POST, request.FILES,
                    instance=existing_application
                    )
        else:
            form = JobApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.speciality = job.speciality


            if existing_application:
                # Reset status to 'Applied'
                # when updating an existing application
                application.status = 0
                application.save()
                messages.success(
                    request,
                    "Your application has been updated" +
                    "and will be reviewed again."
                    )
                return redirect('profile', pk=request.user.pk)

            else:
                # Set initial status for new applications
                application.status = 0
                application.save()
                messages.success(
                    request,
                    "Thank you for your application." +
                    "It will be reviewed shortly."
                )
                # Redirect to Star Rating page
                return redirect('rate_job', job_id=job.id)

    else:
        # If it´s a GET request, show the form (pre-Fill if editing)
        if existing_application:
            form = JobApplicationForm(instance=existing_application)
        else:
            form = JobApplicationForm()

    return render(
        request,
        'jobs/job_detail.html',
        {'job': job,
         'form': form,
         'is_editing': bool(existing_application),
         'star_range': star_range,
         'half_star': half_star,
         }
    )


def rate_job_view(request, job_id):
    job = get_object_or_404(Job, pk=job_id)

    if request.method == 'POST':
        rating_form = JobRatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.cleaned_data['rating']
            job.stars = rating
            job.save()
            messages.success(request, "Thank you for rating the job!")
            # Redirect back to the speciality view with the list of jobs
            return redirect('speciality_jobs',
                            speciality=job.speciality.name
                            )

    else:
        rating_form = JobRatingForm()

    return render(
        request,
        'jobs/rate_job.html',
        {'job': job,
         'rating_form': rating_form}
    )


def job_application_delete_view(request, pk):
    """
    View to delete a job application.
    """
    application = get_object_or_404(
        JobApplication, pk=pk,
        applicant=request.user
    )

    if application.applicant == request.user:
        application.delete()
        messages.success(request,
                         "Your job application has been deleted!")
    else:
        messages.error(request,
                       "You can only delete your own job application.")
    # Redirect to the user´s profile using the pk
    return redirect('profile', pk=request.user.pk)


# Speciality View
class SpecialityView(ListView):
    """View to see all the jobs in a certain speciality
    """
    template_name = 'jobs/speciality.html'
    context_object_name = 'jobs'
    paginate_by = 9

    def get_queryset(self):
        speciality_name = self.kwargs['speciality']
        return Job.objects.filter(speciality__name=speciality_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['speciality_name'] = self.kwargs['speciality']
        # Range for star ratings (1-5)
        context['star_range'] = range(1, 6)
        return context


def speciality_list(request):
    speciality_list = Speciality.objects.exclude(name='other')
    context = {
        'speciality_list': speciality_list
    }
    return context
