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
    print("def carro(request)")
    return control_carro(request)

@login_required
def cargar_datos(request):
    print("def cargar_datos(request)")
    return cargar_dat(request)

@login_required
def nuevo_producto(request, producto_id):
    print("def nuevo_producto(request, producto_id)")
    if request.method == 'POST':  
        producto_id = request.POST.get('producto')
        if producto_id:
            agregar_producto(request, producto_id)      
    return redirect("carro:carro")

@login_required
def agregar_producto(request, producto_id):
    print("def agregar_producto(request, producto_id)")
    carro = Carro(request)
    producto = Producto.objects.get(id=producto_id)
    cantidad_producto_carro = carro.obtener_cantidad_producto(producto)

    # es_edicion = "nro_pedido" in request.session
    agregado = False

    if cantidad_producto_carro == 0:
        if chequear_stock(request, producto, cantidad_producto_carro):
            carro.agregar(producto=producto)
            agregado = True
    else:
        if chequear_cantidad(request, producto, cantidad_producto_carro):
            carro.agregar(producto=producto)
            agregado = True
            
    # =========================
    # PEDIDO EXISTENTE
    # =========================
    # if es_edicion:
    #     if str(producto.categoria) == "Pizzas":
    #         nueva_cantidad = float(cantidad_producto_carro) + 0.5
    #     else:
    #         nueva_cantidad = cantidad_producto_carro + 1

    #     if chequear_actualizacion(request, producto, nueva_cantidad):
    #         carro.agregar(producto=producto)
    #         agregado = True


    # =========================
    # PEDIDO NUEVO
    # =========================
    # else:
        # if cantidad_producto_carro == 0:
        #     if chequear_stock(request, producto, cantidad_producto_carro):
        #         carro.agregar(producto=producto)
        #         agregado = True


    # if not agregado:
    #     messages.error(
    #         request,
    #         mark_safe(
    #             f"<strong>STOCK:</strong><br>"
    #             f"{producto.categoria}: {producto.categoria.cantidad} unidades.<br>"
    #             f"{producto}: {producto.cantidad} unidades."
    #         )
    #     )
    if not agregado:
        mensaje = "<strong>STOCK:</strong><br>"

        # Stock de la categoría
        if not producto.categoria.stock or float(producto.categoria.cantidad) == 0.0:
            mensaje += f"{producto.categoria}: SIN STOCK.<br>"
        else:
            mensaje += f"{producto.categoria}: {producto.categoria.cantidad} unidades.<br>"

        # Stock del producto
        if not producto.stock or float(producto.cantidad) == 0.0:
            mensaje += f"{producto}: SIN STOCK."
        else:
            mensaje += f"{producto}: {producto.cantidad} unidades."

        messages.error(request, mark_safe(mensaje))

    return redirect("carro:carro")

@login_required
def restar_producto(request, producto_id):
    print("def restar_producto(request, producto_id)")
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.restar_producto(producto=producto)
    return redirect("carro:carro")

@login_required
def actualizar_cantidad(request, producto_id):
    print("def actualizar_cantidad(request, producto_id)")
    carro = Carro(request)
    nueva_cantidad = float(request.POST.get("cantidad"))
    producto = Producto.objects.get(id=producto_id)
    
    # es_edicion = "nro_pedido" in request.session
    agregado = False
    
    # # =========================
    # # PEDIDO EXISTENTE
    # # =========================
    # if es_edicion:
    #     pass
    # # =========================
    # # PEDIDO NUEVO
    # # =========================
    # else:
    if chequear_actualizacion(request, producto, nueva_cantidad):
        carro.actualizar_cant(producto=producto, nueva_cantidad=nueva_cantidad)
        agregado = True   

    # if not agregado:
    #     messages.error(
    #         request,
    #         mark_safe(
    #             f"<strong>STOCK:</strong><br>"
                
    #             if producto.categoria.stock == False:
    #                 f"{producto.categoria}: SIN STOCK.<br>"
    #             else
    #                 f"{producto.categoria}: {producto.categoria.cantidad} unidades.<br>"
    #             if producto.stock == False:
    #                 f"{producto}: SIN STOCK.<br>"
    #             else
    #                 f"{producto}: {producto.cantidad} unidades."
                
    #         )
    #     )
    if not agregado:
        mensaje = "<strong>STOCK:</strong><br>"

        # Stock de la categoría
        if not producto.categoria.stock or float(producto.categoria.cantidad) == 0.0:
            mensaje += f"{producto.categoria}: SIN STOCK.<br>"
        else:
            mensaje += f"{producto.categoria}: {producto.categoria.cantidad} unidades.<br>"

        # Stock del producto
        if not producto.stock or float(producto.cantidad) == 0.0:
            mensaje += f"{producto}: SIN STOCK."
        else:
            mensaje += f"{producto}: {producto.cantidad} unidades."

        messages.error(request, mark_safe(mensaje))

    return redirect("carro:carro")

@login_required
def eliminar_producto(request, producto_id):
    print("def eliminar_producto(request, producto_id)")
    carro=Carro(request)
    producto=Producto.objects.get(id=producto_id)
    carro.eliminar(producto=producto)
    return redirect("carro:carro")

@login_required
def limpiar_carro(request):
    print("def limpiar_carro(request)")
    carro=Carro(request)
    carro.limpiar_carro()
    if 'nro_pedido' in request.session:
                    del request.session['nro_pedido']
    return redirect("pedido:listar_pendientes")



