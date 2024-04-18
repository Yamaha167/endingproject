from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse

def welcome(request):
    return render(request, 'welcome.html')

def about(request):
    return render(request, 'about.html')

def games(request):
    return render(request, 'games.html')