from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from productos.models import Producto
from pedido.models import FormaEntrega

from .select_productos import select_productos
from .carro import Carro
from facturas.models import Caja
from .control_carro import control_carro, cargar_dat

@login_required
def carro(request):
    return control_carro(request)

@login_required
def cargar_datos(request):
    return cargar_dat(request)

@login_required
def nuevo_producto(request, producto_id):
    if request.method == 'POST':  
        producto_id = request.POST.get('producto')
        if producto_id:
            agregar_producto(request, producto_id)      
    return redirect("carro:carro")

@login_required
def agregar_producto(request, producto_id):
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.agregar(producto=producto)
    return redirect("carro:carro")

@login_required
def restar_producto(request, producto_id):
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.restar_producto(producto=producto)
    return redirect("carro:carro")

@login_required
def actualizar_cantidad(request, producto_id):
    carro = Carro(request)
    nueva_cantidad = request.POST.get('cantidad')
    producto_id = producto_id 
    producto = Producto.objects.get(id=producto_id)
    carro.actualizar_cant(producto=producto, nueva_cantidad=nueva_cantidad)   
    return redirect("carro:carro")

@login_required
def eliminar_producto(request, producto_id):
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.eliminar(producto=producto)
    return redirect("carro:carro")

@login_required
def limpiar_carro(request):
    carro=Carro(request)
    carro.limpiar_carro()
    if 'nro_pedido' in request.session:
                    del request.session['nro_pedido']
    return redirect("pedido:listar_pendientes")
