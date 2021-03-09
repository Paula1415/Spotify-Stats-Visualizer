from django.urls import path

from . import views

urlpatterns = [
    path('yourstats/', views.chartsAndStats, name='all-charts'),
]