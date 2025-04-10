from pedido.models import Pedido, PedidoProductos, PedidosReservado, PedidosProductosReservados
from productos.models import Producto

def recuperar_pedidos():
    pedidos_datos = Pedido.objects.all()
    productos_pedidos = PedidoProductos.objects.all()
    pedidos_reserv_datos = PedidosReservado.objects.all()
    productos_reserv_pedidos = PedidosProductosReservados.objects.all()
    
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
                
    pedidos_reserv = {pedido.id: 
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
     
     } for pedido in pedidos_reserv_datos}
                       
    for key, value in pedidos_reserv.items():
        for producto in productos_reserv_pedidos:
            if key == producto.pedido.id:
                producto_ped = Producto.objects.get(id=producto.producto.id)
                pedidos_reserv[producto.pedido.id][str(producto.producto.id)] = {                  
                    "producto_id": int(producto.producto.id),
                    "nombre": str(producto_ped.nombre),
                    "precio_unit": str(producto_ped.precio_unit),
                    "precio_media": str(producto_ped.precio_media),
                    "precio_doc": str(producto_ped.precio_doc),
                    "cantidad": float(producto.cantidad),
                    "subtotal": float(producto.subtotal),   
                    "categoria": str(producto_ped.categoria.nombre)
                    } 
                
    return {"pedidos": pedidos, "pedidos_reservados": pedidos_reserv}

def recuperar_pendientes():
    pedidos_datos = Pedido.objects.filter(estado='pendiente')
    productos_pedidos = PedidoProductos.objects.all()
    pedidos_reserv_datos = PedidosReservado.objects.filter(estado='pendiente')
    productos_reserv_pedidos = PedidosProductosReservados.objects.all()
    
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
                
    pedidos_reserv = {pedido.id: 
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
     
     } for pedido in pedidos_reserv_datos}
                       
    for key, value in pedidos_reserv.items():
        for producto in productos_reserv_pedidos:
            if key == producto.pedido.id:
                producto_ped = Producto.objects.get(id=producto.producto.id)
                pedidos_reserv[producto.pedido.id][str(producto.producto.id)] = {                  
                    "producto_id": int(producto.producto.id),
                    "nombre": str(producto_ped.nombre),
                    "precio_unit": str(producto_ped.precio_unit),
                    "precio_media": str(producto_ped.precio_media),
                    "precio_doc": str(producto_ped.precio_doc),
                    "cantidad": float(producto.cantidad),
                    "subtotal": float(producto.subtotal),   
                    "categoria": str(producto_ped.categoria.nombre)
                    } 
                
    return {"pedidos": pedidos, "pedidos_reservados": pedidos_reserv}

def recuperar_entregados():
    pedidos_datos = Pedido.objects.filter(estado='entregado')
    productos_pedidos = PedidoProductos.objects.all()
    pedidos_reserv_datos = PedidosReservado.objects.filter(estado='entregado')
    productos_reserv_pedidos = PedidosProductosReservados.objects.all()
    
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
                
    pedidos_reserv = {pedido.id: 
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
     
     } for pedido in pedidos_reserv_datos}
                       
    for key, value in pedidos_reserv.items():
        for producto in productos_reserv_pedidos:
            if key == producto.pedido.id:
                producto_ped = Producto.objects.get(id=producto.producto.id)
                pedidos_reserv[producto.pedido.id][str(producto.producto.id)] = {                  
                    "producto_id": int(producto.producto.id),
                    "nombre": str(producto_ped.nombre),
                    "precio_unit": str(producto_ped.precio_unit),
                    "precio_media": str(producto_ped.precio_media),
                    "precio_doc": str(producto_ped.precio_doc),
                    "cantidad": float(producto.cantidad),
                    "subtotal": float(producto.subtotal),   
                    "categoria": str(producto_ped.categoria.nombre)
                    } 
                
    return {"pedidos": pedidos, "pedidos_reservados": pedidos_reserv}

def recuperar_reservados():
    pedidos_datos = Pedido.objects.filter(estado='reservado')
    productos_pedidos = PedidoProductos.objects.all()
    pedidos_reserv_datos = PedidosReservado.objects.filter(estado='reservado')
    productos_reserv_pedidos = PedidosProductosReservados.objects.all()
    
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
                
    pedidos_reserv = {pedido.id: 
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
     
     } for pedido in pedidos_reserv_datos}
                       
    for key, value in pedidos_reserv.items():
        for producto in productos_reserv_pedidos:
            if key == producto.pedido.id:
                producto_ped = Producto.objects.get(id=producto.producto.id)
                pedidos_reserv[producto.pedido.id][str(producto.producto.id)] = {                  
                    "producto_id": int(producto.producto.id),
                    "nombre": str(producto_ped.nombre),
                    "precio_unit": str(producto_ped.precio_unit),
                    "precio_media": str(producto_ped.precio_media),
                    "precio_doc": str(producto_ped.precio_doc),
                    "cantidad": float(producto.cantidad),
                    "subtotal": float(producto.subtotal),   
                    "categoria": str(producto_ped.categoria.nombre)
                    } 
                
    return {"pedidos": pedidos, "pedidos_reservados": pedidos_reserv}