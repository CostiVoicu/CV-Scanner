from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Profile, KeyWord

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()

    return render(request, 'profiles_page.html', {'profiles_list': profiles})

def profile_details(request, id):
    profile = get_object_or_404(Profile, pk=id)
    keywords = profile.keywords.all()

    return render(request, 'detail.html', {'profile': profile, 'keywords': keywords})

def add_profile(request):
    if request.method == 'POST':
        profile_name = request.POST.get('profile_name')
        keywords_text = request.POST.get('keywords')
        
        profile = Profile.objects.create(name=profile_name)

        add_keywords(keywords_text, profile)

    return render(request, 'add_profile.html')
    
def add_keywords(keywords_text, profile):
    for line in keywords_text.splitlines():
        words = line.split(':')
        KeyWord.objects.create(profile=profile, name=words[0], value=words[1])