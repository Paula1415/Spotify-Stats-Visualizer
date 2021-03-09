from django.urls import path
from .views import AuthURL, spotify_callback
from . import views

urlpatterns = [
    path('', views.landingPage, name = 'landingpage'),
    path('get-auth-url/', AuthURL.as_view()),
    path('redirect/',spotify_callback)
]