from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import Profile, KeyWord
from django.urls import reverse
from .forms import ProfileForm, KeyWordFormSet

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()

    context = {
        'profiles_list': profiles
    }

    return render(request, 'profiles_page.html', context)

def profile_details(request, id):
    profile = get_object_or_404(Profile, pk=id)
    keywords = profile.keywords.all()

    context = {
        'profile': profile, 
        'keywords': keywords
    }

    return render(request, 'detail.html', context)

def add_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save()
            keyword_formset = KeyWordFormSet(request.POST, instance=profile)
            if keyword_formset.is_valid():
                keyword_formset.save()
                return redirect('edit', id=profile.id)
    else:
        profile_form = ProfileForm()
        keyword_formset = KeyWordFormSet()
    
    context = {
        'profile_form': profile_form,
        'keyword_formset': keyword_formset,
    }
    return render(request, 'add_profile.html', context)

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

            for form in keyword_formset.forms:
                if 'delete_button' in request.POST and request.POST.get('delete_button') == str(form.instance.pk):
                    if form.instance.pk:
                        form.instance.delete()

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