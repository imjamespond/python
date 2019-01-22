from django.shortcuts import render
from django.http import HttpResponse

from .models import Frame

# Create your views here.

def index(request):
    return render(request, 'build/index.html')
