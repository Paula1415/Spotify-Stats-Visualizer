from django.shortcuts import render, redirect
from decouple import config
from requests import Request, post
from django.views.generic.base import View

class AuthURL(View):
    def get(self, request, format=None):
        scopes = 'user-top-read '
        Request('GET','https://accounts.spotify.com/authorize', params = {
            'scope':scopes,
            'response': 'code',
            'redirect': config('REDIRECT_URI'),
            'client_id' : config('SPOTIFY_CLIENT_ID')
        })

def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data = {
        'grant_type': 'authorization_code',
        'code' : code,
        'redirect_uri': config('REDIRECT_URI'),
        'client_secret': config('SPOTIFY_CLIENT_SECRET')

    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token')
    refresh_token =  response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    return redirect('charts:chartsAndStats')




def landingPage(request):
    return render(request, 'landingpage.html')