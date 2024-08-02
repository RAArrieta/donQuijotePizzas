from pedido.models import Pedido, PedidoProductos
from productos.models import Producto

def recuperar_pedidos():
    pedidos_datos = Pedido.objects.all()
    productos_pedidos = PedidoProductos.objects.all()
    
    pedidos = {pedido.id: 
    {'datos': {  
        "estado": pedido.estado,
        "pago": pedido.pago,
        "forma_entrega": pedido.forma_entrega.forma_entrega,
        "precio_entrega": pedido.forma_entrega.precio,
        "envio":pedido.forma_entrega.envio,
        "nombre": pedido.nombre,
        "direccion": pedido.direccion,
        "observacion": pedido.observacion,
        "total":pedido.total,
        # "estado": str(pedido.estado),
        # "pago": str(pedido.pago),
        # "forma_entrega": str(pedido.forma_entrega.forma_entrega),
        # "precio_entrega": float(pedido.forma_entrega.precio),
        # "envio":bool(pedido.forma_entrega.envio),
        # "nombre": str(pedido.nombre),
        # "direccion": str(pedido.direccion),
        # "observacion": str(pedido.observacion),
        # "total":float(pedido.total),
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