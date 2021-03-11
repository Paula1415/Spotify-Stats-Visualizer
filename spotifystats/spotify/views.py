from django.shortcuts import render, redirect
from decouple import config
from requests import Request, Session
from urllib.parse import urlparse

class spotify_authentication:

    def getauth(self, request, format=None):
        scopes = 'user-top-read '
        response = Request('GET','https://accounts.spotify.com/authorize', params = {
            'client_id' : config('SPOTIFY_CLIENT_ID'),
            'scope':scopes,
            'response_type': 'code',
            'redirect_uri': config('REDIRECT_URI'),
        }).prepare().url
        redirect_url = redirect(response)
        self.code = request.GET.get('code')
        return redirect_url

    def landingPage(self, request, format=None):
        context= {}
        context['code'] = self.code
        return render(request, 'landingpage.html', context)
