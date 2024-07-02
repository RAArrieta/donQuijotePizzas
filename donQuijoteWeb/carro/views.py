from django.shortcuts import render, redirect
from productos.models import Producto
from .pedido_productos import Carro, select_productos
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "carro/index.html")

@login_required
def carro(request):
    categorias=select_productos() 
    carro=Carro(request)
    comprobacion_pedido=carro.comprobacion_pedido()
    datos = {
                "estado": "",
                "pago": "",
                "forma_entrega": "envio",
                "nombre": "",
                "direccion": "",
                "observacion": "",
            }
    
    if request.method == 'GET':  
        producto_id = request.GET.get('producto')
        if producto_id:
            agregar_producto(request, producto_id)
            
    for field in ['estado', 'pago', 'forma_entrega', 'direccion', 'nombre', 'observacion']:
        if field in request.GET:
            datos[field]=request.GET.get(field)
            
            if field == 'forma_entrega' and datos["forma_entrega"] != "envio":
                datos["direccion"]= "RETIRA POR SUCURSAL"

            carro.agregar_datos(datos=datos)
            
    
    # if 'estado' in request.GET:
    #     estado = request.GET.get('estado')
    #     datos = {"estado": estado}
    #     carro.agregar_datos(datos=datos)
        
    # if 'pago' in request.GET:
    #     pago = request.GET.get('pago')
    #     datos = {"pago": pago}
    #     carro.agregar_datos(datos=datos)
        
    # if 'forma_entrega' in request.GET:
    #     forma_entrega = request.GET.get('forma_entrega')
    #     if forma_entrega == "envio":
    #         datos = {"forma_entrega": forma_entrega}
    #     else:
    #         datos = {"forma_entrega": forma_entrega, "direccion": "RETIRA POR SUCURSAL"}
    #     carro.agregar_datos(datos=datos)
                
    # if 'direccion' in request.GET: 
    #     direccion = request.GET.get('direccion')
    #     datos = {"direccion": direccion}
    #     carro.agregar_datos(datos=datos)
        
    # if 'nombre' in request.GET: 
    #     nombre = request.GET.get('nombre')
    #     datos = {"nombre": nombre}
    #     carro.agregar_datos(datos=datos)
        
    # if 'observacion' in request.GET: 
    #     observacion = request.GET.get('observacion')
    #     datos = {"observacion": observacion}
    #     carro.agregar_datos(datos=datos)      
        
    if 'cargar_pedido' in request.GET:
        if comprobacion_pedido:
            return redirect("pedido:procesar_ped")
          
    context = {
        'categorias': categorias,
        'datos': datos,
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
