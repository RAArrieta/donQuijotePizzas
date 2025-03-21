from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from pedido.models import FormaEntrega, Pedido, PedidoProductos
from carro.carro import Carro
from pedido.recuperar_pedidos import recuperar_pedidos


def procesar_pedido(request):
    nro_pedido = request.session.pop('nro_pedido', None)
    carro = Carro(request)
    lista_productos = list()
    pedido = None

    if nro_pedido:
        pedido = Pedido.objects.filter(id=nro_pedido).first()

    for key, value in carro.carro.items():
        if key != "datos" and key != "empanadas":
            lista_productos.append(PedidoProductos(
                producto_id=key,
                cantidad=value["cantidad"],
                subtotal=value["subtotal"],
                pedido=pedido
            ))
        elif key == "datos":
            forma_entrega_nombre = value["forma_entrega"]
            forma_entrega_obj = get_object_or_404(FormaEntrega, forma_entrega=forma_entrega_nombre)

            if pedido:
                pedido.estado = value["estado"]
                pedido.pago = value["pago"]
                pedido.forma_entrega = forma_entrega_obj
                pedido.precio_entrega= value["precio_entrega"]
                pedido.nombre = value["nombre"]
                pedido.direccion = value["direccion"]
                pedido.observacion = value["observacion"]
                pedido.total = value["total"]
            else:
                pedido = Pedido.objects.create(
                    estado=value["estado"],
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
        PedidoProductos.objects.filter(pedido=pedido).delete()
        for producto in lista_productos:
            producto.pedido = pedido
        PedidoProductos.objects.bulk_create(lista_productos)
        
    carro.limpiar_carro()  
    
def mod_pedido(request, pedido):
    nro_pedido_actual = request.session.get('nro_pedido')  
    nro_pedido_nuevo = pedido 
    
    if nro_pedido_actual is not None and str(nro_pedido_actual) != str(nro_pedido_nuevo):
        return redirect(reverse("pedido:modificar_pedido", args=[nro_pedido_actual]))
    
    pedidos = recuperar_pedidos()
    pedido = pedidos[nro_pedido_nuevo]
    carro = Carro(request)
    carro.cargar_pedido(pedido)
    request.session['nro_pedido'] = nro_pedido_nuevo