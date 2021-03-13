import tekore as tk
from decouple import config

class getuserdata:

    def getauth(self):
        conf = (config('SPOTIFY_CLIENT_ID'), config('SPOTIFY_CLIENT_SECRET'), config('REDIRECT_URI'))
        scopes = 'user-top-read'
        Token = tk.RefreshingCredentials(*conf)
        return Token

    def getdata(self, token):
        spotify = tk.Spotify(token)
        tracks = spotify.current_user_top_tracks()
        return tracks
