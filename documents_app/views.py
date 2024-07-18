from cv_scanner_script import get_top_doc
from django.shortcuts import render, get_object_or_404
from profiles.models import Profile, KeyWord
from django.forms.models import model_to_dict

# Create your views here.

def scanner(request):
    job_profiles = Profile.objects.all()

    if request.method == 'POST':
        persons_count = request.POST.get('persons_count')
        selected_job_profile_id = request.POST.get('job_profile')
        documents = request.FILES.getlist('documents')
        documents_names = [doc.name for doc in documents]
        
        selected_job_profile = get_object_or_404(Profile, pk=selected_job_profile_id)

        keywords = selected_job_profile.keywords.all().values('name', 'value')
        keywords = convertor_to_custom_format(keywords)

        top_persons = get_top_doc(files=documents,no_persons=int(persons_count), key_words=keywords)

    context = {
        'job_profiles': job_profiles
    }

    return render(request, 'documents_page.html', context)

def convertor_to_custom_format(dict):
    result_dict = {}

    for item in dict:
        result_dict[item['name']] = item['value']

    return result_dict