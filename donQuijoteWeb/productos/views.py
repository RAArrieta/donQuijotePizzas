from django.shortcuts import render
from .models import Producto

def home(request):
    productos = Producto.objects.select_related('categoria').all()
    context = {
        'object_list': productos
    }
    return render(request, 'productos/index.html', context)
