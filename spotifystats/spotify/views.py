from django.shortcuts import render, redirect
from decouple import config
from requests import Request, post,get
from urllib.parse import urlparse
from .authHandling import getuserdata



def getauth(request):
    token = getuserdata()
    token.getauth()

def getUserdata(request):
    # data = getuserdata()
    # tracks = data.getdata()
    # context = {'userdata' : tracks}
    return render(request, 'userdata.html')

def landingPage(request):
    return render(request, 'landingpage.html')
