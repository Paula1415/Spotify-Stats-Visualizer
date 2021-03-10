from django.shortcuts import render, redirect
from decouple import config
from requests import Request

def getauth(request):
    scopes = 'user-top-read '
    response = Request('GET','https://accounts.spotify.com/authorize', params = {
        'client_id' : config('SPOTIFY_CLIENT_ID'),
        'scope':scopes,
        'response_type': 'token',
        'redirect_uri': config('REDIRECT_URI'),
    }).prepare().url
    redirect_url = redirect(response)
    return redirect_url



def landingPage(request):
    return render(request, 'landingpage.html')
