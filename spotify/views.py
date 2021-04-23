from django.shortcuts import render, redirect
from decouple import config
from requests import Request, post,get
from urllib.parse import urlparse
from .authHandling import getuserdata
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from django.http import HttpResponse
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
from .task import task

spotify = getuserdata()

def getauth(request):
    return spotify.getauth(request)

def callback(request):
    return spotify.spotify_callback(request)


def getuserdata(request):
    return spotify.userdata(request)

def no_data(request):
    return render(request, 'nodata.html')

def landingPage(request):
    return render(request, 'landingpage.html')

def on_error(request):
    return render(request, 'onerror.html', context={ 'auth': 'http://127.0.0.1:8000/get-auth-url/'})

scheduler = ''
def waiting_page(request):
    task(request)
    return HttpResponse('waiting...')
