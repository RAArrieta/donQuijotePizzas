from django.shortcuts import render
from .tesoreria import tesoreria

def home(request):
    return tesoreria(request)