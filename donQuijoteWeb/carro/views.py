from django.shortcuts import render, redirect
from productos.models import Producto
from .pedido_productos import Carro, select_productos
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "carro/index.html")

@login_required
def carro(request):
    datos = {
                "estado": "Pendiente",
                "pago": "Cobrar",
                "forma_entrega": "Retira",
                "nombre": "nombre",
                "direccion": "direccion",
                "observacion": "observacion",
            }
    
    categorias=select_productos()
    if request.method == 'GET':      
        producto_id = request.GET.get('producto')
        if producto_id:
            return agregar_producto(request, producto_id)
        
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
def agregar_datos(request):
    if request.method == 'GET':
        direccion = request.GET.get('direccion')
        nombre = request.GET.get('nombre')
        observacion = request.GET.get('observacion')
        
        if direccion and nombre and observacion:
            print("Estoy en agregar datos")
            carro = Carro(request)
            datos = {"direccion": direccion, "nombre": nombre, "observacion": observacion}
            carro.agregar_datos(datos=datos)
            return redirect("pedido:procesar_ped")
        
        # Manejar el caso donde los datos no estén presentes
        return render(request, 'core:home')

# @login_required
# def agregar_datos(request, direccion, nombre, observacion):
#     print("Estoy en agregar datos")
#     carro=Carro(request)
#     datos={"direccion":direccion, "nombre":nombre, "observacion":observacion}
#     carro.agregar_datos(datos=datos)
#     return redirect("carro:carro")

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
