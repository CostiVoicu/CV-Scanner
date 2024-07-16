from django.shortcuts import render

# Create your views here.

def add_documents(request):
    return render(request, 'documents/add_documents_page.html')