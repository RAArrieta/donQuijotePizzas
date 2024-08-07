from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from productos.models import Producto
from pedido.models import FormaEntrega

from .select_productos import select_productos
from .carro import Carro

@login_required
def carro(request):
    cargar_datos(request)
    carro=Carro(request)
    categorias=select_productos() 
    forma_entrega = FormaEntrega.objects.all()
    comprobacion_pedido=carro.comprobacion_pedido()
    cargar_pedido = request.GET.get('cargar_pedido', 'false') == 'true'
    print("ESTOY EN CARRO")
    if cargar_pedido:
        print("ENTRO A IF")
        if comprobacion_pedido:
            print("COMPRUEBO TRUE")
            return redirect("pedido:procesar_ped")   
    
    context = {
        'categorias': categorias,
        'forma_entrega': forma_entrega,
    }
        
    return render(request, "carro/carro.html", context)

@login_required
def cargar_datos(request):
    carro=Carro(request)
    datos = {
            "estado": "",
            "pago": "",
            "forma_entrega": "",
            "precio_entrega": "",
            "envio":"",
            "nombre": "",
            "direccion": "",
            "observacion": "",
        }
    if request.method == 'POST':        
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
    carro.calcular_precio()
    return redirect("carro:carro")

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
    return redirect("pedido:home")
