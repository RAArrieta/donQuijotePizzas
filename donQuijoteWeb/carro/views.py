from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from productos.models import Producto
from pedido.models import FormaEntrega

from .select_productos import select_productos
from .carro import Carro

@login_required
def carro(request):
    categorias=select_productos() 
    forma_entrega = FormaEntrega.objects.all()
    carro=Carro(request)
    comprobacion_pedido=carro.comprobacion_pedido()
    datos = {
                "estado": "",
                "pago": "",
                "forma_entrega": "envio",
                "precio_entrega": "",
                "envio":"",
                "nombre": "",
                "direccion": "",
                "observacion": "",
            }
    
    if request.method == 'POST':  
        producto_id = request.POST.get('producto')
        if producto_id:
            agregar_producto(request, producto_id)
            
    for field in ['estado', 'pago', 'direccion', 'forma_entrega', 'nombre', 'observacion']:
        if field in request.POST:
            datos[field]=request.POST.get(field)
            if field == 'forma_entrega':
                entrega_id = request.POST.get("forma_entrega")
                entrega = FormaEntrega.objects.get(id=entrega_id)
                datos["forma_entrega"]= entrega.forma_entrega
                datos["precio_entrega"]= entrega.precio
                datos["envio"]= entrega.envio
            carro.agregar_datos(datos=datos)   

    if 'cargar_pedido' in request.POST:
        if comprobacion_pedido:
            return redirect("pedido:procesar_ped")   
     
    comprobacion_pedido=carro.comprobacion_pedido()
    total= carro.importe_total_carro()
    
    context = {
        'categorias': categorias,
        'datos': datos,
        'forma_entrega': forma_entrega,
        'total': total,
    }
        
    return render(request, "carro/carro.html", context)

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

@csrf_exempt
def actualizar_cantidad(request, producto_id):
    if request.method == 'POST':
        cantidad = request.POST.get('cantidad')
        producto_id = producto_id 

    carro = Carro(request)
    nueva_cantidad = cantidad
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
    return redirect("pedido:home")
