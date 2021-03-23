import tekore as tk
from decouple import config
from requests import Request
from django.shortcuts import redirect, render
import json
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt
import mpld3
import seaborn as sns

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
        tracks = spotify.current_user_top_tracks(time_range = 'medium_term', limit=50, offset=0)
        tracks_name = [t.name for t in tracks.items]
        #get audio analysis of top user tracks
        tracks_ids = [i.id for i in tracks.items]
        usertracks_audio_features = spotify.tracks_audio_features(tracks_ids).json()
        usertracks_data  = pd.read_json(io.StringIO(usertracks_audio_features))
        user_df = pd.DataFrame(data = usertracks_data)
        user_df['name'] = tracks_name
        # user_df.to_excel('usertracks.xlsx')
        #plot the data
        plot = user_df.plot()
        fig_user = plot.get_figure()
        html_user = mpld3.fig_to_html(fig_user)

        #get audio analysis of top 50 global
        top_50_global = spotify.playlist_items(playlist_id='37i9dQZEVXbMDoHDwVN2tF',offset=0,limit=50).json()
        top_50_global = json.loads(top_50_global)
        top_50_global = [n["track"] for n in top_50_global["items"]]
        top_50_global_names = [n['name'] for n in top_50_global]
        top_50_global_ids = [n['id'] for n in top_50_global]
        globaltracks_audio_features = spotify.tracks_audio_features(top_50_global_ids).json()
        # create dataframe
        global_data  = pd.read_json(io.StringIO(globaltracks_audio_features))
        global_df = pd.DataFrame(data = global_data)
        global_df['name'] = top_50_global_names
        global_df.to_excel('globaltracks.xlsx')

        #plot the data
        plot = global_df.plot()
        fig = plot.get_figure()
        html_global = mpld3.fig_to_html(fig)

        sns.set_theme()
        catplot = sns.catplot(data=user_df, kind="swarm", x="energy", y="valence")
        catplot_fig = catplot.fig
        catplot_render = mpld3.fig_to_html(catplot_fig)

        context = {'tracks' : tracks_name,  'user_plot': html_user, 'global_plot': html_global, 'catplot': catplot_render}
        # return render(request, 'userdata.html', context)
        return render(request, 'userdata.html', context)





