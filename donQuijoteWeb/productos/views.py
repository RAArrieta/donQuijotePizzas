from django.shortcuts import render

def home(request):
    return render(request, 'productos/index.html')
