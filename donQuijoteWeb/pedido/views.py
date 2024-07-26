from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from pedido.models import FormaEntrega
from pedido.forms import FormaEntregaForm
from django.views.generic import (UpdateView,)
from django.contrib.auth.mixins import LoginRequiredMixin

from carro.pedido_productos import Carro
from pedido.models import Pedido, PedidoProductos
from django.shortcuts import get_object_or_404

@login_required
def home(request):
    return render(request, "pedido/index.html")

@login_required
def procesar_ped(request):
    carro=Carro(request)
    lista_productos=list()
    pedido = None
    
    for key, value in carro.carro.items():
        print(f"key: {key}, value: {value}")
        if key != "datos" and key != "empanadas":
            lista_productos.append(PedidoProductos(
            
                producto_id=key,
                cantidad=value["cantidad"],
                pedido=pedido
                
            ))
        elif key == "datos":
            forma_entrega_nombre = value["forma_entrega"]
            forma_entrega_obj = get_object_or_404(FormaEntrega, forma_entrega=forma_entrega_nombre)
            
            pedido = Pedido.objects.create(
                estado=value["estado"],
                pago=value["pago"],
                forma_entrega=forma_entrega_obj,
                nombre=value["nombre"],
                direccion=value["direccion"],
                observacion=value["observacion"],
                total=value["total"],
            )
            
    if pedido: 
        for producto in lista_productos:
            producto.pedido = pedido
        
        PedidoProductos.objects.bulk_create(lista_productos)
    
    carro.limpiar_carro()
    
    return redirect("pedido:home")    

class FormaEntregaUpdate(LoginRequiredMixin, UpdateView):
    model = FormaEntrega
    form_class = FormaEntregaForm
    success_url = reverse_lazy("productos:home")
    
    