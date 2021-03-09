from django.shortcuts import render
from decouple import config
from requests import Request, post

class AuthURL():
    def get(self, request, format=None):
        scopes = 'user-top-read '
        url = Request('GET','https://accounts.spotify.com/authorize', params = {
            'scope':scopes,
            'response': 'code',
            'redirect': config('REDIRECT_URI')
        })





def landingPage(request):
    return render(request, 'landingpage.html')