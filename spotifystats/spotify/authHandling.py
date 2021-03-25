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
import numpy as np

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
        user_df['playlist'] = 'Your Top 50 Tracks'

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
        global_df['playlist'] = 'Top 50: Global'


        # get audio analysis of today top hits
        top_50_today = spotify.playlist_items(playlist_id='37i9dQZF1DXcBWIGoYBM5M',offset=0,limit=50).json()
        top_50_today = json.loads(top_50_today)
        top_50_today = [n["track"] for n in top_50_today["items"]]
        top_50_today_names = [n['name'] for n in top_50_today]
        top_50_today_ids = [n['id'] for n in top_50_today]
        globaltoday_audio_features = spotify.tracks_audio_features(top_50_today_ids).json()
        # create dataframe
        today_global_data  = pd.read_json(io.StringIO(globaltoday_audio_features))
        today_global_df = pd.DataFrame(data = today_global_data)
        today_global_df['name'] = top_50_today_names
        today_global_df['playlist'] = "Today's Top Hits"


        frames_to_merge = [user_df, global_df, today_global_df]
        tidy_frame = pd.concat(frames_to_merge)
        # tidy_frame.to_excel('tidyframe.xlsx')

        df1_melt = pd.melt(user_df, id_vars=['playlist'], var_name='property')
        df2_melt = pd.melt(global_df, id_vars=['playlist'], var_name='property')
        df3_melt = pd.melt(today_global_df, id_vars=['playlist'],var_name='property')

        #------------- Organizing dataframes from wide to long for plotting barplot-------------------------

        ## ----------------user dataframe---------------
        df1_melt_nonnumeric = df1_melt[df1_melt['value'].apply(lambda x: type(x) in [int, np.int64, float, np.float64])]
        df1_melt_nonnumeric['value'] = pd.to_numeric(df1_melt_nonnumeric['value'])

        df1_melt_mean = df1_melt_nonnumeric.groupby(['property']).mean(numeric_only = True)
        df1_melt_mean['playlist'] = 'Your Top 50 Tracks'

        ##-----------------global dataframe -------------------------
        df2_melt_nonnumeric = df2_melt[df2_melt['value'].apply(lambda x: type(x) in [int, np.int64, float, np.float64])]
        df2_melt_nonnumeric['value'] = pd.to_numeric(df2_melt_nonnumeric['value'])

        df2_melt_mean = df2_melt_nonnumeric.groupby(['property']).mean(numeric_only = True)
        df2_melt_mean['playlist'] = 'Top Global 50'


        ##-----------------top hits dataframe -----------------------------
        df3_melt_nonnumeric = df3_melt[df3_melt['value'].apply(lambda x: type(x) in [int, np.int64, float, np.float64])]
        df3_melt_nonnumeric['value'] = pd.to_numeric(df3_melt_nonnumeric['value'])

        df3_melt_mean = df3_melt_nonnumeric.groupby(['property']).mean(numeric_only = True)
        df3_melt_mean['playlist'] = 'Top 50 daily Hits'

        ##----------- concat all long dataframes ------------------------------
        numeric_only_frames = [df1_melt_mean, df2_melt_mean, df3_melt_mean]
        long_frame = pd.concat(numeric_only_frames)
        long_frame2 = long_frame.reset_index()
        long_frame2.to_excel('longframe.xlsx')


        #-----------PLOTS----------------------------------------
        # scatterplot
        stripplot = sns.scatterplot(data=tidy_frame, x="energy", y="valence", hue="playlist")
        stripplot_fig = stripplot.get_figure()
        stripplot_render = mpld3.fig_to_html(stripplot_fig)


        #bar catplot
        bar_catplot = sns.catplot(
            data=long_frame2, kind="violin",
            x="property", y="value", hue="playlist", legend=True
        )
        bar_catplot_figure = bar_catplot.fig
        catplot_render = mpld3.fig_to_html(bar_catplot_figure)


        context = {'tracks' : tracks_name, 'stripplot': stripplot_render, 'bar_catplot': catplot_render}
        # return render(request, 'userdata.html', context)
        return render(request, 'userdata.html', context)





