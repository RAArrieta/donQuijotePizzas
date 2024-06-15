from django.shortcuts import render
from .models import Producto

def home(request):
    productos= Producto.objects.all()
    print(productos)
    return render(request, 'productos/index.html', {"productos":productos})
