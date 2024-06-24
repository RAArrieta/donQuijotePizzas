from django.shortcuts import render, redirect
from productos.models import Producto
from .funciones import Carro, select_productos
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "carro/index.html")

@login_required
def carro(request):
    categorias=select_productos()
    if request.method == 'GET':
        producto_id = request.GET.get('producto')
        print(f"producto_id en carro {producto_id}")
        if producto_id:
            return agregar_producto(request, producto_id)
        
    context = {
        'categorias': categorias,
    }

    return render(request, "carro/carro.html", context)

@login_required
def agregar_producto(request, producto_id):
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.agregar(producto=producto)
    return redirect("carro:carro")

@login_required
def eliminar_producto(request, producto_id):
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.eliminar(producto=producto)
    return redirect("carro:carro")

@login_required
def restar_producto(request, producto_id):
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.restar_producto(producto=producto)
    return redirect("carro:carro")

@login_required
def limpiar_carro(request):
    carro=Carro(request)
    carro.limpiar_carro()
    return redirect("carro:carro")
