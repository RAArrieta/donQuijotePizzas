from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (UpdateView)
from django.contrib import messages

from pedido.models import FormaEntrega
from pedido.forms import FormaEntregaForm

from pedido.procesar_pedido import procesar_pedido, mod_pedido
from pedido.recuperar_pedidos import recuperar_pedidos, recuperar_pendientes, recuperar_entregados, recuperar_reservados

@login_required
def procesar_ped(request):   
    procesar_pedido(request)
    return redirect("pedido:listar_pendientes")

class FormaEntregaUpdate(LoginRequiredMixin, UpdateView):
    model = FormaEntrega
    form_class = FormaEntregaForm
    success_url = reverse_lazy("productos:home")

@login_required
def modificar_pedido(request, pedido):
    mod_pedido(request, pedido)
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


    
    