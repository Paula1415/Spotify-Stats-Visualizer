from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage, name = 'landingpage'),
    path('get-auth-url/', views.getauth),
    path('callback/', views.callback),
    path('Stats/', views.getuserdata),
    path('nodata/', views.no_data),
    path('error/', views.on_error)

]
