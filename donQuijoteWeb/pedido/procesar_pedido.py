from pyexpat.errors import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from pedido.models import FormaEntrega, Pedido, PedidoProductos, PedidosReservado, PedidosProductosReservados
from carro.carro import Carro
from pedido.recuperar_pedidos import recuperar_pedidos

from productos.models import Producto
from carro.chequear_cantidad import recheq_stock_pedido

def procesar_pedido(request):
    nro_pedido = request.session.pop('nro_pedido', None)
    carro = Carro(request)
    lista_productos = []
    pedido = None
    es_reservado = False 
    
    # print(carro.carro)
    # print(carro.carro["datos"]["tipo"]) 
    


    if nro_pedido:
        pedido = Pedido.objects.filter(id=nro_pedido).first()
        if not pedido:
            pedido = PedidosReservado.objects.filter(id=nro_pedido).first()
            if pedido:
                es_reservado = True

    for key, value in carro.carro.items():
        if key != "datos" and key != "empanadas":
            if es_reservado:
                lista_productos.append(PedidosProductosReservados(
                    producto_id=key,
                    cantidad=value["cantidad"],
                    subtotal=value["subtotal"],
                    pedido=pedido
                ))
            else:
                lista_productos.append(PedidoProductos(
                    producto_id=key,
                    cantidad=value["cantidad"],
                    subtotal=value["subtotal"],
                    pedido=pedido
                ))
        elif key == "datos":
            forma_entrega_nombre = value["forma_entrega"]
            forma_entrega_obj = get_object_or_404(FormaEntrega, forma_entrega=forma_entrega_nombre)
            estado_pedido = value["estado"]
            
            
            
            if estado_pedido.lower() == "reservado":
                es_reservado = True

            if pedido:
                pedido.estado = estado_pedido
                pedido.pago = value["pago"]
                pedido.forma_entrega = forma_entrega_obj
                pedido.precio_entrega = value["precio_entrega"]
                pedido.nombre = value["nombre"]
                pedido.direccion = value["direccion"]
                pedido.observacion = value["observacion"]
                pedido.total = value["total"]
            else:
                modelo_pedido = PedidosReservado if es_reservado else Pedido
                pedido = modelo_pedido.objects.create(
                    estado=estado_pedido,
                    pago=value["pago"],
                    forma_entrega=forma_entrega_obj,
                    precio_entrega=value["precio_entrega"],
                    nombre=value["nombre"],
                    direccion=value["direccion"],
                    observacion=value["observacion"],
                    total=value["total"],
                )
            pedido.save()
        elif key == "empanadas":
            cantidad_emp = value["cantidad"]
            subtotal_emp = value["subtotal_emp"]
            if pedido:
                pedido.cantidad_emp = cantidad_emp
                pedido.subtotal_emp = subtotal_emp
                pedido.save()
                
    # if not recheq_stock_pedido(request):
    
    #     print("Redirecciono por falta de stock")
    #     return redirect("carro:carro")            
    
    if pedido:
        # Elegimos el modelo correspondiente
        modelo_producto = PedidosProductosReservados if es_reservado else PedidoProductos

        # 👉 1. Devolver stock de productos anteriores
        productos_previos = modelo_producto.objects.filter(pedido=pedido)
        for item in productos_previos:
            producto = item.producto
            categoria = producto.categoria
            producto.cantidad += item.cantidad
            categoria.cantidad += item.cantidad
            producto.save()
            categoria.save()

        # 👉 2. Borrar productos anteriores del pedido
        productos_previos.delete()

        # 👉 3. Crear productos nuevos
        modelo_producto.objects.bulk_create(lista_productos)

        # 👉 4. Descontar stock por los nuevos productos
        productos_actualizados = {}
        categorias_actualizadas = {}

        for item in lista_productos:
            producto = item.producto
            categoria = producto.categoria

            # Acumular cantidad a descontar por producto
            if producto.id not in productos_actualizados:
                productos_actualizados[producto.id] = producto
            productos_actualizados[producto.id].cantidad -= item.cantidad

            # Acumular cantidad a descontar por categoría
            if categoria.id not in categorias_actualizadas:
                categorias_actualizadas[categoria.id] = categoria
            categorias_actualizadas[categoria.id].cantidad -= item.cantidad

        # 👉 5. Guardar cambios en productos y categorías
        for producto in productos_actualizados.values():
            producto.save()

        for categoria in categorias_actualizadas.values():
            categoria.save()

    carro.limpiar_carro()
    return redirect("pedido:listar_pendientes")

    
def mod_pedido(request, tipo, pedido):
    nro_pedido_actual = request.session.get('nro_pedido')  
    nro_pedido_nuevo = pedido 

    if nro_pedido_actual is not None and str(nro_pedido_actual) != str(nro_pedido_nuevo):
        return redirect(reverse("pedido:modificar_pedido", args=[tipo, nro_pedido_actual]))

    datos_pedidos = recuperar_pedidos()  
    if tipo == "normal":
        pedidos = datos_pedidos.get("pedidos", {})
    else:  
        pedidos = datos_pedidos.get("pedidos_reservados", {})

    
    pedido = pedidos.get(nro_pedido_nuevo)
    if not pedido:
        messages.error(request, "El pedido no existe.")
        return redirect(reverse("pedido:home"))

    carro = Carro(request)
    carro.cargar_pedido(pedido)

    request.session['nro_pedido'] = nro_pedido_nuevo
    request.session['tipo_pedido'] = tipo