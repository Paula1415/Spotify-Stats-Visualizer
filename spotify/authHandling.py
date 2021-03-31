import tekore as tk
from decouple import config
from requests import Request
from django.shortcuts import redirect, render
import json
import pandas as pd
from io import BytesIO, StringIO
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import textwrap

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
        if error:
            return redirect('https://spotistats-visualizer.herokuapp.com/error')
        credentials= tk.Credentials(*conf)
        not_refreshing_user_token = credentials.request_user_token(str(code))
        self.refreshing_user_token = tk.RefreshingToken(not_refreshing_user_token, credentials)
        return redirect('https://spotistats-visualizer.herokuapp.com/Stats')

    def userdata(self,request):
        #instanciate spotify class
        spotify = tk.Spotify(self.refreshing_user_token)
        #get user top tracks
        tracks = spotify.current_user_top_tracks(time_range = 'medium_term', limit=50, offset=0)
        tracks_items = [t for t in tracks.items]
        if not tracks_items:
            return redirect('https://spotistats-visualizer.herokuapp.com/nodata')
        else:
            tracks_name = [t.name for t in tracks.items]
            #get audio analysis of top user tracks
            tracks_ids = [i.id for i in tracks.items]
            # get artists
            artists = spotify.current_user_top_artists(time_range = 'medium_term', limit=10, offset=0)
            artist_name = [t.name for t in artists.items]
            usertracks_audio_features = spotify.tracks_audio_features(tracks_ids).json()
            usertracks_data  = pd.read_json(StringIO(usertracks_audio_features))
            user_df = pd.DataFrame(data = usertracks_data)
            user_df['name'] = tracks_name
            user_df['playlist'] = 'Your Top 50 Tracks'
            # here
            user_df_nameindex = user_df.truncate(after=4)
            user_df['name'] = ['\n'.join(textwrap.wrap(x, 12)) for x in  user_df['name']]
            index = user_df['name'].truncate(after=4)
            user_df_nameindex2 = user_df_nameindex.set_index(index)
            user_df_nameindex2 = user_df_nameindex2.drop(columns=['id', 'analysis_url','time_signature', 'track_href', 'type', 'uri', 'name' ,'playlist', 'duration_ms', 'tempo', 'loudness', 'mode', 'key'])
            # user_df_nameindex2.to_excel('nameasindex.xlsx')

            userdf_nottruncated = user_df.drop(columns=['id', 'analysis_url','time_signature', 'track_href', 'type', 'uri', 'name' ,'playlist', 'duration_ms', 'tempo', 'loudness', 'key', 'mode'])



            #get audio analysis of top 50 global
            top_50_global = spotify.playlist_items(playlist_id='37i9dQZEVXbMDoHDwVN2tF',offset=0,limit=50).json()
            top_50_global = json.loads(top_50_global)
            top_50_global = [n["track"] for n in top_50_global["items"]]
            top_50_global_names = [n['name'] for n in top_50_global]
            top_50_global_ids = [n['id'] for n in top_50_global]
            globaltracks_audio_features = spotify.tracks_audio_features(top_50_global_ids).json()
            # create dataframe
            global_data  = pd.read_json(StringIO(globaltracks_audio_features))
            global_df = pd.DataFrame(data = global_data)
            global_df['name'] = top_50_global_names
            global_df['playlist'] = 'Top 50: Global'

            global_df_numeric = global_df.drop(columns=['id', 'analysis_url','time_signature', 'track_href', 'type', 'uri', 'name' ,'playlist', 'duration_ms', 'tempo', 'loudness', 'key', 'mode', 'instrumentalness'])


            # get audio analysis of today top hits
            top_50_today = spotify.playlist_items(playlist_id='37i9dQZF1DXcBWIGoYBM5M',offset=0,limit=50).json()
            top_50_today = json.loads(top_50_today)
            top_50_today = [n["track"] for n in top_50_today["items"]]
            top_50_today_names = [n['name'] for n in top_50_today]
            top_50_today_ids = [n['id'] for n in top_50_today]
            globaltoday_audio_features = spotify.tracks_audio_features(top_50_today_ids).json()
            # create dataframe
            today_global_data  = pd.read_json(StringIO(globaltoday_audio_features))
            today_global_df = pd.DataFrame(data = today_global_data)
            today_global_df['name'] = top_50_today_names
            today_global_df['playlist'] = "Today's Top Hits"

            today_global_df_numeric = today_global_df.drop(columns=['id', 'analysis_url','time_signature', 'track_href', 'type', 'uri', 'name' ,'playlist', 'duration_ms', 'tempo', 'loudness', 'key', 'mode', 'instrumentalness'])


            frames_to_merge = [user_df, global_df, today_global_df]
            tidy_frame = pd.concat(frames_to_merge)
            # tidy_frame.to_excel('tidyframe.xlsx')
            onlynum_tidyframe = tidy_frame.drop(['id', 'analysis_url', 'duration_ms','key', 'loudness', 'tempo', 'time_signature', 'track_href', 'type', 'uri', 'name'], axis=1)

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
            final_long_frame = long_frame2.astype({'property': str})
            final_long_frame= final_long_frame.drop([2, 5, 7, 10, 11, 15, 18,20,  23, 24, 28, 31,33, 36, 37 ])
            df1_melt_mean_reset = df1_melt_mean.reset_index()

            #-----------PLOTS----------------------------------------
            # scatterplot
            sns.set_style("darkgrid")
            plt.style.use('dark_background')
            matplotlib.rc('axes', facecolor = '#5e5e5e')
            matplotlib.rc('grid', color = '#8c8c8c', linestyle ='solid')
            plt.grid(color='w', linestyle='solid')
            matplotlib.rc('xtick', direction='out', color='gray')
            matplotlib.rc('ytick', direction='out', color='gray')
            matplotlib.rc('lines', linewidth=2)

            stripplot = sns.scatterplot(data=tidy_frame, x="energy", y="valence", hue="playlist",palette="mako", s=100)
            scatterplot_tmpfile = BytesIO()
            stripplot.figure.savefig(scatterplot_tmpfile, format ='png', facecolor="#1b1b1b")
            plt.close()
            encoded = base64.b64encode(scatterplot_tmpfile.getvalue()).decode('utf-8')
            stripplot_render = r"<img src='data:image/png;base64,{}'>".format(encoded)

            #bar catplot
            bar_catplot = sns.catplot(
                kind="bar",data=final_long_frame, x="property", y= "value", palette="mako", hue="playlist", legend=True)
            bar_catplot.fig.suptitle("mean values of the audio features")
            for axes in bar_catplot.axes.flat:
                _ = axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
            plt.tight_layout()

            # encode the plot to base64 because mpld3 don't support cat data
            bar_tmpfile = BytesIO()
            bar_catplot.savefig(bar_tmpfile, format ='png', facecolor="#1b1b1b")
            plt.close()
            encoded = base64.b64encode(bar_tmpfile.getvalue()).decode('utf-8')
            catplot_render = r"<img src='data:image/png;base64,{}'>".format(encoded)
            #heatmap

            heatmap = sns.heatmap(data=user_df_nameindex2, annot=True, linewidth=0.5, linecolor='#8c8c8c', cmap="mako")
            heatmap_tmpfile = BytesIO()
            heatmap.figure.savefig(heatmap_tmpfile, format ='png', bbox_inches = "tight", facecolor="#1b1b1b")
            plt.close()
            heatmap_encoded = base64.b64encode(heatmap_tmpfile.getvalue()).decode('utf-8')
            heatmap_render = r"<img src='data:image/png;base64,{}'>".format(heatmap_encoded)

            # user kde
            kde_plot = sns.kdeplot(data=userdf_nottruncated, palette="mako", shade=True)
            kde_tmpfile = BytesIO()
            kde_plot.figure.savefig(kde_tmpfile, format ='png', facecolor="#1b1b1b")
            plt.close()
            encoded_kde = base64.b64encode(kde_tmpfile.getvalue()).decode('utf-8')
            kde_render = r"<img src='data:image/png;base64,{}'>".format(encoded_kde)

            #global kde
            global_kde_plot = sns.kdeplot(data=global_df_numeric, palette="mako", fill=True)
            global_kde_tmpfile = BytesIO()
            global_kde_plot.figure.savefig(global_kde_tmpfile, format ='png', facecolor="#1b1b1b")
            plt.close()
            global_encoded_kde = base64.b64encode(global_kde_tmpfile.getvalue()).decode('utf-8')
            global_kde_render = r"<img src='data:image/png;base64,{}'>".format(global_encoded_kde)

            #today top hits kde

            kde_plot_todhits = sns.kdeplot(data=today_global_df_numeric, palette="mako", fill=True)
            todhits_kde_tmpfile = BytesIO()
            kde_plot_todhits.figure.savefig(todhits_kde_tmpfile, format ='png', facecolor="#1b1b1b")
            plt.close()
            todhits_encoded_kde = base64.b64encode(todhits_kde_tmpfile.getvalue()).decode('utf-8')
            todhits_kde_render = r"<img src='data:image/png;base64,{}'>".format(todhits_encoded_kde)

            facetgrid= sns.catplot(data=tidy_frame,x = 'valence', y='danceability', col='playlist', palette='mako')
            for axes in facetgrid.axes.flat:
                __ = axes.set_xticklabels([])
            plt.tight_layout()
            facet_tmpfile = BytesIO()
            facetgrid.savefig(facet_tmpfile, format ='png', facecolor="#1b1b1b")
            plt.close()
            facet_encoded = base64.b64encode(facet_tmpfile.getvalue()).decode('utf-8')
            facet_render = r"<img src='data:image/png;base64,{}'>".format(facet_encoded)

            context = {'tracks' : tracks_name, 'stripplot': stripplot_render, 'bar_catplot': catplot_render, 'heatmap': heatmap_render,  'kdeplot': kde_render, 'todaykde': todhits_kde_render, 'globalkde': global_kde_render, 'artists': artist_name , 'facetplot':facet_render}

            return render(request, 'userdata.html', context)






