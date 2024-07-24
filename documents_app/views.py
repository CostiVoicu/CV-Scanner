from cv_scanner_script import get_top_doc
from django.shortcuts import render, get_object_or_404, redirect
from profiles.models import Profile
import base64

# Create your views here.

def scanner(request):
    job_profiles = Profile.objects.all()
    count_error  = ''

    if request.method == 'POST':
        persons_count = request.POST.get('persons_count')
        selected_job_profile_id = request.POST.get('job_profile')
        documents = request.FILES.getlist('documents')

        count_error = scanner_error_check(int(persons_count))

        if count_error == '':
            selected_job_profile = get_object_or_404(Profile, pk=selected_job_profile_id)

            keywords = selected_job_profile.keywords.all().values('name', 'value')
            keywords = convertor_to_custom_format(keywords)

            top_persons = get_top_doc(files=documents,no_persons=int(persons_count), key_words=keywords)

            file_data_urls = []

            for pdf_file in top_persons:
                pdf_file.seek(0)
                base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
                data_url = f"data:application/pdf;base64,{base64_pdf}"
                file_data_urls.append(data_url)

            context = {
                'file_data_urls': file_data_urls
            }

            return render(request, 'results_page.html', context)
    
    context = {
        'job_profiles': job_profiles,
        'count_error': count_error
    }

    return render(request, 'documents_page.html', context)

def convertor_to_custom_format(dict):
    result_dict = {}

    for item in dict:
        result_dict[item['name']] = item['value']

    return result_dict

def scanner_error_check(persons_count):
    count_error =  ''

    if persons_count < 0:
        count_error = 'Persons Count can\'t be negative!'
    if persons_count == 0:
        count_error = 'Persons Count can\'t be zero!'

    return count_error