from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from carro.pedido_productos import Carro
from pedido.models import Pedido, PedidoProductos


@login_required
def procesar_ped(request):
    pedido=Pedido.objects.create()
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
                estado="Pendiente",
                pago="Cobrar",
                nombre=value["nombre"],
                direccion=value["direccion"],
                observacion=value["observacion"]
            )
            
        
    PedidoProductos.objects.bulk_create(lista_productos)
    
    carro.limpiar_carro()
    
    return redirect("carro:home")
    
    