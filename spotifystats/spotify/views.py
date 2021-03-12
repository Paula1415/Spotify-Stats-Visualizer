from django.shortcuts import render, redirect
from decouple import config
from requests import Request, post,get
from urllib.parse import urlparse
import tekore as tk


token = ''
def getauth(request):
    global token
    conf = (config('SPOTIFY_CLIENT_ID'), config('SPOTIFY_CLIENT_SECRET'), config('REDIRECT_URI'))
    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)


def getUserdata(request):
    global token
    spotify = tk.Spotify(token)
    tracks = spotify.current_user_top_tracks()
    context = {'userdata': tracks}
    return render(request, 'userdata.html', context)

def landingPage(request):
    return render(request, 'landingpage.html')
