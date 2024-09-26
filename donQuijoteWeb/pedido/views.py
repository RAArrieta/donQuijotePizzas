from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (UpdateView,)

from pedido.models import FormaEntrega, Pedido, PedidoProductos
from pedido.forms import FormaEntregaForm
from pedido.recuperar_pedidos import recuperar_pedidos, recuperar_pendientes, recuperar_entregados, recuperar_reservados
from carro.carro import Carro
from django.contrib import messages
from facturas.models import Caja

@login_required
def procesar_ped(request):   
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
    return redirect("pedido:listar_pendientes")
   

class FormaEntregaUpdate(LoginRequiredMixin, UpdateView):
    model = FormaEntrega
    form_class = FormaEntregaForm
    success_url = reverse_lazy("productos:home")
    
@login_required
def modificar_pedido(request, pedido):
    nro_pedido = pedido
    pedidos = recuperar_pedidos()
    pedido = pedidos[nro_pedido]
    carro = Carro(request)
    carro.cargar_pedido(pedido)
    request.session['nro_pedido'] = nro_pedido
    return redirect("carro:carro")
    
@login_required
def listar_pedidos(request):
    pedidos = recuperar_pedidos()
    if not pedidos:
        messages.warning(request, "No hay pedidos cargados...")
    return render(request, 'pedido/index.html', {'pedidos': pedidos})


@login_required
def listar_pendientes(request):
    pedidos = recuperar_pendientes()
    if not pedidos:
        messages.warning(request, "No hay pedidos pendientes...")
    return render(request, 'pedido/index.html', {'pedidos': pedidos})

@login_required
def listar_entregados(request):
    pedidos = recuperar_entregados()
    if not pedidos:
        messages.warning(request, "No hay pedidos entregados...")
    return render(request, 'pedido/index.html', {'pedidos': pedidos})

@login_required
def listar_reservados(request):
    pedidos = recuperar_reservados()
    if not pedidos:
        messages.warning(request, "No hay pedidos reservados...")
    return render(request, 'pedido/index.html', {'pedidos': pedidos})


    
    