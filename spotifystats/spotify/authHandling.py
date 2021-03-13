import tekore as tk
from decouple import config
from requests import Request
from django.shortcuts import redirect, render

class getuserdata:
    def __init__(self):
        self.refreshing_user_token = None
    def getauth(self, request):
        # redirect the user to spotify auth and ask for permission, return code to be exchanged for token and refresh token
        scopes = 'user-top-read '
        response = Request('GET','https://accounts.spotify.com/authorize', params = {
        'client_id' : config('SPOTIFY_CLIENT_ID'),
        'scope':scopes,
        'response_type': 'code',
        'redirect_uri': config('REDIRECT_URI'),
        }).prepare().url
        redirect_url = redirect(response)
        return redirect_url

    def spotify_callback(self, request):
        conf = (config('SPOTIFY_CLIENT_ID'), config('SPOTIFY_CLIENT_SECRET'), config('REDIRECT_URI'))
        code = request.GET.get('code')
        error = request.GET.get('error')
        credentials= tk.Credentials(*conf)
        not_refreshing_user_token = credentials.request_user_token(str(code))
        self.refreshing_user_token = tk.RefreshingToken(not_refreshing_user_token, credentials)
        return redirect('http://127.0.0.1:8000/Stats/')

    def userdata(self,request):
        spotify = tk.Spotify(self.refreshing_user_token)
        tracks = spotify.current_user_top_tracks(time_range = 'medium_term', limit=10, offset=0)
        tracks = [t.name for t in tracks.items]
        context = {'userdata' : tracks}
        return render(request, 'userdata.html', context)






