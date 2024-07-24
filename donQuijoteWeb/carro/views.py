from django.shortcuts import render, redirect
from productos.models import Producto
from pedido.models import FormaEntrega
from .pedido_productos import Carro, select_productos
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "carro/index.html")

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
                "total":0.0,
            }
    
    if request.method == 'GET':  
        producto_id = request.GET.get('producto')
        if producto_id:
            agregar_producto(request, producto_id)
            
    for field in ['estado', 'pago', 'direccion', 'forma_entrega', 'nombre', 'observacion']:
        if field in request.GET:
            datos[field]=request.GET.get(field)
            if field == 'forma_entrega':
                entrega_id = request.GET.get("forma_entrega")
                entrega = FormaEntrega.objects.get(id=entrega_id)
                datos["forma_entrega"]= entrega.forma_entrega
                datos["precio_entrega"]= entrega.precio
                datos["envio"]= entrega.envio
            carro.agregar_datos(datos=datos)   
        
    if 'cargar_pedido' in request.GET:
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

@login_required
def actualizar_cantidad(request, producto_id):   
    if request.method == 'POST':    
        carro = Carro(request)       
        nueva_cantidad = float(request.POST['nueva_cantidad'])
        producto_id = request.POST['producto_id']
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
    return redirect("carro:carro")
