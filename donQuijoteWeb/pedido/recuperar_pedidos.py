from pedido.models import Pedido, PedidoProductos, PedidosReservado, PedidosProductosReservados
from productos.models import Producto
from facturas.models import Caja

def recuperar_pedidos(key):
    if key:
        pedidos_datos = Pedido.objects.filter(estado=key)
        productos_pedidos = PedidoProductos.objects.all()
        pedidos_reserv_datos = PedidosReservado.objects.filter(estado=key)
        productos_reserv_pedidos = PedidosProductosReservados.objects.all()
    else:
        pedidos_datos = Pedido.objects.all()
        productos_pedidos = PedidoProductos.objects.all()
        pedidos_reserv_datos = PedidosReservado.objects.filter()
        productos_reserv_pedidos = PedidosProductosReservados.objects.all()
        
    pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)
    pedidos_reserv = cargar_recuperos(pedidos_reserv_datos, productos_reserv_pedidos)
                  
    return {"pedidos": pedidos, "pedidos_reservados": pedidos_reserv}

def recuperar_sin_reservados(modelo_pedido, modelo_producto, key):
    pedidos_datos = modelo_pedido.objects.exclude(
        estado__in=['reservado', 'cancelado']
    )

    productos_pedidos = modelo_producto.objects.all()

    pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)

    return {key: pedidos}

def cargar_recuperos(pedidos_datos, productos_pedidos):
    pedidos = {pedido.id: 
    {'datos': {  
        "tipo": pedido.tipo,
        "estado": pedido.estado,
        "hora": pedido.hora.isoformat(),  
        "pago": pedido.pago,
        "forma_entrega": pedido.forma_entrega.forma_entrega,
        "precio_entrega": pedido.forma_entrega.precio,
        "envio":pedido.forma_entrega.envio,
        "nombre": pedido.nombre,
        "direccion": pedido.direccion,
        "observacion": pedido.observacion,
        "total":pedido.total,
        },
     'empanadas': {
        "cantidad":pedido.cantidad_emp,
        "subtotal_emp":pedido.subtotal_emp,
     }
     
     } for pedido in pedidos_datos}
    
    for key, value in pedidos.items():
        for producto in productos_pedidos:
            if key == producto.pedido.id:
                producto_ped = Producto.objects.get(id=producto.producto.id)
                pedidos[producto.pedido.id][str(producto.producto.id)] = {                  
                    "producto_id": int(producto.producto.id),
                    "nombre": str(producto_ped.nombre),
                    "precio_unit": str(producto_ped.precio_unit),
                    "precio_media": str(producto_ped.precio_media),
                    "precio_doc": str(producto_ped.precio_doc),
                    "cantidad": float(producto.cantidad),
                    "subtotal": float(producto.subtotal),   
                    "categoria": str(producto_ped.categoria.nombre)
                    } 
                
    return pedidos
    
def obtener_estado_caja():
    caja = Caja.objects.first()

    if caja:
        return caja.estado_caja
    return False