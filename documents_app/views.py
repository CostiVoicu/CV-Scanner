from django.shortcuts import render
from profiles.models import Profile, KeyWord

# Create your views here.

def scanner(request):
    job_profiles = Profile.objects.all()

    if request.method == 'POST':
        persons_count = request.POST.get('persons_count')
        selected_job_profile = request.POST.get('job_profile')
        documents = request.FILES.getlist('documents')

    context = {
        'job_profiles': job_profiles
    }

    return render(request, 'documents_page.html', context)