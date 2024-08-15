from pedido.models import Pedido

def counter_pedidos(request):
    cant_pedidos = Pedido.objects.all().count()
    cant_entregados = Pedido.objects.filter(estado='entregado').count()
    cant_pendientes = Pedido.objects.filter(estado='pendiente').count()
    cant_reservados = Pedido.objects.filter(estado='reservado').count()
    
    return {'cant_pedidos':cant_pedidos, "cant_entregados":cant_entregados, "cant_pendientes":cant_pendientes, "cant_reservados":cant_reservados }