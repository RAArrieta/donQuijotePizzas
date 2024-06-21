from django.shortcuts import render
from productos.models import Producto
from . import funciones
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "carro/index.html")

@login_required
def carro(request):
    categorias=funciones.select_productos()
    return render(request, "carro/carro.html", {"categorias": categorias})



