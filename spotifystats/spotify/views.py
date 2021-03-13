from django.shortcuts import render, redirect
from decouple import config
from requests import Request, post,get
from urllib.parse import urlparse
from .authHandling import getuserdata


spotify = getuserdata()

def getauth(request):
    return spotify.getauth(request)

def callback(request):
    return spotify.spotify_callback(request)

def getuserdata(request):
    return spotify.userdata(request)

def landingPage(request):
    return render(request, 'landingpage.html')
