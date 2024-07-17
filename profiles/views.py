from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import Profile, KeyWord
from django.urls import reverse
from .forms import ProfileForm, KeyWordFormSet

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

def delete_profile(request, id):
    Profile.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('profile_list'))

def edit_profile(request, id):
    profile = get_object_or_404(Profile, id=id)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        keyword_formset = KeyWordFormSet(request.POST, instance=profile)
        
        if profile_form.is_valid() and keyword_formset.is_valid():
            profile_form.save()
            keyword_formset.save()
            return redirect('edit', id=profile.id)
    else:
        profile_form = ProfileForm(instance=profile)
        keyword_formset = KeyWordFormSet(instance=profile)
    
    context = {
        'profile_form': profile_form,
        'keyword_formset': keyword_formset,
        'profile': profile
    }

    return render(request, 'edit_profile.html', context)