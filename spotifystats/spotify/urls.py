from django.urls import path
from .views import spotify_authentication


urlpatterns = [
    path('', spotify_authentication.landingPage, name = 'landingpage'),
    path('get-auth-url/', spotify_authentication.getauth)
]
