from django.shortcuts import render

def homepage(request):
    return render(request, 'home_page.html')