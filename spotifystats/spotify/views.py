from django.shortcuts import render, redirect
from decouple import config
from requests import Request, post
from urllib.parse import urlparse



def getauth(request):
    scopes = 'user-top-read '
    response = Request('GET','https://accounts.spotify.com/authorize', params = {
        'client_id' : config('SPOTIFY_CLIENT_ID'),
        'scope':scopes,
        'response_type': 'code',
        'redirect_uri': config('REDIRECT_URI'),
        }).prepare().url
    redirect_url = redirect(response)
    return redirect_url

access_token = 0
def spotify_callback (request):
    global access_token
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': config('REDIRECT_URI'),
        'client_id': config('SPOTIFY_CLIENT_ID'),
        'client_secret': config('SPOTIFY_CLIENT_SECRET')
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    redirection = redirect('http://127.0.0.1:8000/')
    return redirection

def landingPage(request):
    global access_token
    context ={'tok' : access_token}
    return render(request, 'landingpage.html', context)
