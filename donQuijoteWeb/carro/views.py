from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from productos.models import Producto

from .carro import Carro
from .control_carro import control_carro, cargar_dat
from .chequear_cantidad import chequear_stock, chequear_cantidad, chequear_actualizacion

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
    cantidad_carro = carro.obtener_cantidad_producto(producto)
    agregado = False

    if chequear_stock(request, producto) and cantidad_carro == 0.0:
        carro.agregar(producto=producto)
        agregado = True
    elif chequear_cantidad(request, producto, cantidad_carro):
        carro.agregar(producto=producto)
        agregado = True

    if not agregado:
        messages.error(request, mark_safe(f"<strong>STOCK:</strong><br>{producto.categoria}: {producto.categoria.cantidad} unidades.<br>{producto}: {producto.cantidad} unidades."))

           
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
    nueva_cantidad = float(request.POST.get('cantidad'))
    producto_id = producto_id 
    producto = Producto.objects.get(id=producto_id)
    
    if chequear_actualizacion(request, producto, nueva_cantidad) and nueva_cantidad > 0.0:
        carro.actualizar_cant(producto=producto, nueva_cantidad=nueva_cantidad)
    else:
        messages.error(request, mark_safe(f"<strong>STOCK:</strong><br>{producto.categoria}: {producto.categoria.cantidad} unidades.<br>{producto}: {producto.cantidad} unidades."))
       
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
