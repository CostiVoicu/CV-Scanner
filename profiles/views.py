from django.shortcuts import render, get_object_or_404
from .models import Profile

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()

    return render(request, 'profiles_page.html', {'profiles_list': profiles})

def profile_details(request, id):
    profile = get_object_or_404(Profile, pk=id)
    keywords = profile.keywords.all()

    return render(request, 'detail.html', {'profile': profile, 'keywords': keywords})