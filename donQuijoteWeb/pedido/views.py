from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from pedido.models import FormaEntrega
from pedido.forms import FormaEntregaForm
from django.views.generic import (CreateView, DeleteView, DetailView, UpdateView,)
from django.contrib.auth.mixins import LoginRequiredMixin

from carro.pedido_productos import Carro
from pedido.models import Pedido, PedidoProductos


@login_required
def procesar_ped(request):
    carro=Carro(request)
    lista_productos=list()
    
    for key, value in carro.carro.items():
        print(f"key: {key}, value: {value}")
        if key != "datos":
            lista_productos.append(PedidoProductos(
            
                producto_id=key,
                cantidad=value["cantidad"],
                pedido=pedido
                
            ))
        else:
            pedido=Pedido.objects.create(
                estado=value["estado"],
                pago=value["pago"],
                forma_entrega=value["forma_entrega"],
                nombre=value["nombre"],
                direccion=value["direccion"],
                observacion=value["observacion"]
            )
            
        
    PedidoProductos.objects.bulk_create(lista_productos)
    
    carro.limpiar_carro()
    
    return redirect("carro:home")

class FormaEntregaUpdate(LoginRequiredMixin, UpdateView):
    model = FormaEntrega
    form_class = FormaEntregaForm
    success_url = reverse_lazy("productos:home")
    
    