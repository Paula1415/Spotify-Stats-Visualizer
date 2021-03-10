from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage, name = 'landingpage'),
    path('get-auth-url/', views.getauth),
    # path('redirect/',views.spotify_callback)
]