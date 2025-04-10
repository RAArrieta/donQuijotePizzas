from pyexpat.errors import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from pedido.models import FormaEntrega, Pedido, PedidoProductos, PedidosReservado, PedidosProductosReservados
from carro.carro import Carro
from pedido.recuperar_pedidos import recuperar_pedidos

from productos.models import Producto


def procesar_pedido(request):
    nro_pedido = request.session.pop('nro_pedido', None)
    carro = Carro(request)
    lista_productos = []
    pedido = None
    es_reservado = False  

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

    if pedido:
        # Limpiamos productos previos según el tipo de pedido
        if es_reservado:
            PedidosProductosReservados.objects.filter(pedido=pedido).delete()
            PedidosProductosReservados.objects.bulk_create(lista_productos)
        else:
            PedidoProductos.objects.filter(pedido=pedido).delete()
            PedidoProductos.objects.bulk_create(lista_productos)

    carro.limpiar_carro()  
    
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