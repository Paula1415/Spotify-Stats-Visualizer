import tekore as tk
from decouple import config
from requests import Request
from django.shortcuts import redirect, render
import json
from statistics import mean

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
        #instanciate spotify class
        spotify = tk.Spotify(self.refreshing_user_token)
        #get user top tracks
        tracks = spotify.current_user_top_tracks(time_range = 'medium_term', limit=5, offset=0)
        #get user top artists
        artists = spotify.current_user_top_artists(time_range = 'medium_term', limit=5, offset=0)
        tracks_name = [t.name for t in tracks.items]
        artists = [a.name for a in artists.items]

        #get audio analysis of top user tracks
        tracks_ids = [i.id for i in tracks.items]
        usertracks_audio_features = spotify.tracks_audio_features(tracks_ids)
        usertracks_audio_features = [i.acousticness for i in usertracks_audio_features]
        usertracks_audio_features=mean(usertracks_audio_features)

        #get audio analysis of top 50 global
        top_50_global = spotify.playlist_items(playlist_id='37i9dQZEVXbMDoHDwVN2tF',offset=0, fields=['items.track.id'],limit=5)
        top_50_global= [item for val in top_50_global.values() for item in val]
        top_50_global= [top_50_global[i]['track']['id'] for i in range(len(top_50_global))]
        globaltracks_audio_features = spotify.tracks_audio_features(top_50_global)
        globaltracks_audio_features = [i.acousticness for i in globaltracks_audio_features]
        globaltracks_audio_features = mean(globaltracks_audio_features)

        context = {'tracks' : tracks_name, 'artists': artists, 'top50':globaltracks_audio_features, 'topuser': usertracks_audio_features}
        return render(request, 'userdata.html', context)






