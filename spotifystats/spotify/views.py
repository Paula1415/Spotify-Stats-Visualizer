from django.shortcuts import render, redirect
from decouple import config
from requests import Request, post,get
from urllib.parse import urlparse



response = 0
def getauth(request):
    global response
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
error = 0
def spotify_callback (request):
    global access_token
    global error
    global response

    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        context ={'error' : error, 'auth' : response}
        return render(request, 'onerror.html', context)

    else:
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

        redirection = redirect('http://127.0.0.1:8000/userdata/')
        return redirection


def getUserdata(request):
    global access_token

    usertopreads = get('https://api.spotify.com/v1/me/top/artists', headers ={
        'Authorization' : 'Bearer',
        'token' : str(access_token)
    })

    context = {'userdata' : usertopreads}
    return render(request, 'userdata.html', context)

def landingPage(request):
    return render(request, 'landingpage.html')
