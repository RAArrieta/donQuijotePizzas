from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (UpdateView)
from django.contrib import messages

from pedido.models import FormaEntrega, PedidoProductos, Pedido, PedidosReservado, PedidosProductosReservados
from pedido.forms import FormaEntregaForm
 
from pedido.procesar_pedido import procesar_pedido, mod_pedido
from pedido.recuperar_pedidos import recuperar_pedidos, recuperar_pendientes, recuperar_entregados, recuperar_reservados

@login_required
def procesar_ped(request):   
    return procesar_pedido(request)
    

class FormaEntregaUpdate(LoginRequiredMixin, UpdateView):
    model = FormaEntrega
    form_class = FormaEntregaForm
    success_url = reverse_lazy("productos:home")

@login_required
def modificar_pedido(request, tipo, pedido):
    mod_pedido(request, tipo, pedido)
    return redirect("carro:carro")

@login_required
def listar_pedidos(request):  
    datos_pedidos = recuperar_pedidos()  
    pedidos = datos_pedidos.get("pedidos", {})  
    pedidos_reservados = datos_pedidos.get("pedidos_reservados", {})    
    if not pedidos and not pedidos_reservados:
        messages.warning(request, "No hay pedidos cargados...")

    return render(request, 'pedido/index.html', {'pedidos': pedidos, 'pedidos_reservados': pedidos_reservados})

@login_required
def listar_pendientes(request):
    datos_pedidos = recuperar_pendientes()  
    pedidos = datos_pedidos.get("pedidos", {})  
    pedidos_reservados = datos_pedidos.get("pedidos_reservados", {}) 
    if not pedidos:
        messages.warning(request, "No hay pedidos pendientes...")
    return render(request, 'pedido/index.html', {'pedidos': pedidos, 'pedidos_reservados': pedidos_reservados})

@login_required
def listar_entregados(request):
    datos_pedidos = recuperar_entregados()  
    pedidos = datos_pedidos.get("pedidos", {})  
    pedidos_reservados = datos_pedidos.get("pedidos_reservados", {}) 
    if not pedidos:
        messages.warning(request, "No hay pedidos entregados...")
    return render(request, 'pedido/index.html', {'pedidos': pedidos, 'pedidos_reservados': pedidos_reservados})

@login_required
def listar_reservados(request):
    datos_pedidos = recuperar_reservados()  
    pedidos_reservados = datos_pedidos.get("pedidos_reservados", {}) 
    if not pedidos_reservados:
        messages.warning(request, "No hay pedidos reservados...")
    return render(request, 'pedido/index.html', {'pedidos_reservados': pedidos_reservados})


    
    