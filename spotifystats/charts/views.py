from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login(request):
    return HttpResponse('<h1 style="blue"> you are in the login page </h1>')