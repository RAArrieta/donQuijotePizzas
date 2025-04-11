from pedido.models import Pedido, PedidosReservado

def counter_pedidos(request):
    cant_pedidos = Pedido.objects.all().count()
    cant_entregados = Pedido.objects.filter(estado='entregado').count() + PedidosReservado.objects.filter(estado='entregado').count()
    cant_pendientes = Pedido.objects.filter(estado='pendiente').count() + PedidosReservado.objects.filter(estado='pendiente').count()
    cant_reservados = PedidosReservado.objects.filter(estado='reservado').count()
    cant_cancelado = Pedido.objects.filter(estado='cancelado').count() + PedidosReservado.objects.filter(estado='cancelado').count()
    cant_pedidos = Pedido.objects.all().count() + PedidosReservado.objects.all().count() - cant_cancelado - cant_reservados
    cant_envios = Pedido.objects.exclude(forma_entrega__forma_entrega__icontains="retira").filter(estado='entregado').count() + PedidosReservado.objects.exclude(forma_entrega__forma_entrega__icontains="retira").filter(estado='entregado').count() 
    
    return {
        'cant_pedidos':cant_pedidos, 
        "cant_entregados":cant_entregados, 
        "cant_pendientes":cant_pendientes, 
        "cant_reservados":cant_reservados, 
        "cant_envios":cant_envios 
        }
    
