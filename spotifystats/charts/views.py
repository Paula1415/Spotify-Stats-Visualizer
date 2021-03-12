from django.shortcuts import render
from django.http import HttpResponse
import os
import sys

# Create your views here.

def chartsAndStats(request):
    return render(request, 'statistics.html')

