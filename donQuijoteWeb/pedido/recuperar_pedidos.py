from pedido.models import Pedido, PedidoProductos, PedidosReservado, PedidosProductosReservados
from productos.models import Producto

def recuperar_pedidos():
    pedidos_datos = Pedido.objects.all()
    productos_pedidos = PedidoProductos.objects.all()
    pedidos_reserv_datos = PedidosReservado.objects.filter()
    productos_reserv_pedidos = PedidosProductosReservados.objects.all()
    
    pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)
    pedidos_reserv = cargar_recuperos(pedidos_reserv_datos, productos_reserv_pedidos)
                  
    return {"pedidos": pedidos, "pedidos_reservados": pedidos_reserv}

def recuperar_pendientes():
    pedidos_datos = Pedido.objects.filter(estado='pendiente')
    productos_pedidos = PedidoProductos.objects.all()
    pedidos_reserv_datos = PedidosReservado.objects.filter(estado='pendiente')
    productos_reserv_pedidos = PedidosProductosReservados.objects.all()
    
    pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)
    pedidos_reserv = cargar_recuperos(pedidos_reserv_datos, productos_reserv_pedidos)
                  
    return {"pedidos": pedidos, "pedidos_reservados": pedidos_reserv}

def recuperar_entregados():
    pedidos_datos = Pedido.objects.filter(estado='entregado')
    productos_pedidos = PedidoProductos.objects.all()
    pedidos_reserv_datos = PedidosReservado.objects.filter(estado='entregado')
    productos_reserv_pedidos = PedidosProductosReservados.objects.all()
    
    pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)
    pedidos_reserv = cargar_recuperos(pedidos_reserv_datos, productos_reserv_pedidos)
                  
    return {"pedidos": pedidos, "pedidos_reservados": pedidos_reserv}

def recuperar_reservados():
    pedidos_reserv_datos = PedidosReservado.objects.filter(estado='reservado')
    productos_reserv_pedidos = PedidosProductosReservados.objects.all()
                   
    pedidos_reserv = cargar_recuperos(pedidos_reserv_datos, productos_reserv_pedidos)
                
    return {"pedidos_reservados": pedidos_reserv}

def recuperar_sin_reservados():
    pedidos_datos = Pedido.objects.exclude(estado__in=['reservado', 'cancelado'])
    
    productos_pedidos = PedidoProductos.objects.all()
    
    pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)                
                
    return {"pedidos": pedidos}

def recuperar_sin_reservados2():
    pedidos_datos = PedidosReservado.objects.exclude(estado__in=['reservado', 'cancelado'])
    
    productos_pedidos = PedidosProductosReservados.objects.all()
    
    pedidos_reservados = cargar_recuperos(pedidos_datos, productos_pedidos)                
                
    return {"pedidos_reservados": pedidos_reservados}

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
    
from pedido.models import Pedido, PedidoProductos, PedidosReservado, PedidosProductosReservados


# # =============================
# # RECUPERAR TODOS LOS PEDIDOS
# # =============================
# def recuperar_pedidos():

#     pedidos_datos = Pedido.objects.select_related("forma_entrega")

#     productos_pedidos = PedidoProductos.objects.select_related(
#         "pedido",
#         "producto",
#         "producto__categoria"
#     )

#     pedidos_reserv_datos = PedidosReservado.objects.filter(
#         estado='reservado'
#     ).select_related("forma_entrega")

#     productos_reserv_pedidos = PedidosProductosReservados.objects.select_related(
#         "pedido",
#         "producto",
#         "producto__categoria"
#     )

#     pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)
#     pedidos_reserv = cargar_recuperos(pedidos_reserv_datos, productos_reserv_pedidos)

#     return {"pedidos": pedidos, "pedidos_reservados": pedidos_reserv}


# # =============================
# # RECUPERAR PENDIENTES
# # =============================
# def recuperar_pendientes():

#     pedidos_datos = Pedido.objects.filter(
#         estado='pendiente'
#     ).select_related("forma_entrega")

#     productos_pedidos = PedidoProductos.objects.select_related(
#         "pedido",
#         "producto",
#         "producto__categoria"
#     )

#     pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)

#     return {"pedidos": pedidos}


# # =============================
# # RECUPERAR ENTREGADOS
# # =============================
# def recuperar_entregados():

#     pedidos_datos = Pedido.objects.filter(
#         estado='entregado'
#     ).select_related("forma_entrega")

#     productos_pedidos = PedidoProductos.objects.select_related(
#         "pedido",
#         "producto",
#         "producto__categoria"
#     )

#     pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)

#     return {"pedidos": pedidos}


# # =============================
# # RECUPERAR RESERVADOS
# # =============================
# def recuperar_reservados():

#     pedidos_reserv_datos = PedidosReservado.objects.filter(
#         estado='reservado'
#     ).select_related("forma_entrega")

#     productos_reserv_pedidos = PedidosProductosReservados.objects.select_related(
#         "pedido",
#         "producto",
#         "producto__categoria"
#     )

#     pedidos_reserv = cargar_recuperos(pedidos_reserv_datos, productos_reserv_pedidos)

#     return {"pedidos_reservados": pedidos_reserv}


# # =============================
# # RECUPERAR SIN RESERVADOS
# # =============================
# def recuperar_sin_reservados():

#     pedidos_datos = Pedido.objects.exclude(
#         estado='reservado'
#     ).select_related("forma_entrega")

#     productos_pedidos = PedidoProductos.objects.select_related(
#         "pedido",
#         "producto",
#         "producto__categoria"
#     )

#     pedidos = cargar_recuperos(pedidos_datos, productos_pedidos)

#     return {"pedidos": pedidos}


# # =============================
# # FUNCION BASE RECUPERO
# # =============================
# def cargar_recuperos(pedidos_datos, productos_pedidos):

#     pedidos = {}

#     # Crear estructura base
#     for pedido in pedidos_datos:

#         pedidos[pedido.id] = {
#             'datos': {
#                 "tipo": pedido.tipo,
#                 "estado": pedido.estado,
#                 "hora": pedido.hora.isoformat(),
#                 "pago": pedido.pago,
#                 "forma_entrega": pedido.forma_entrega.forma_entrega,
#                 "precio_entrega": pedido.forma_entrega.precio,
#                 "envio": pedido.forma_entrega.envio,
#                 "nombre": pedido.nombre,
#                 "direccion": pedido.direccion,
#                 "observacion": pedido.observacion,
#                 "total": pedido.total,
#             },
#             'empanadas': {
#                 "cantidad": pedido.cantidad_emp,
#                 "subtotal_emp": pedido.subtotal_emp,
#             }
#         }

#     # Recorrer productos UNA sola vez
#     for producto in productos_pedidos:

#         pedido_id = producto.pedido.id

#         if pedido_id not in pedidos:
#             continue

#         prod = producto.producto

#         pedidos[pedido_id][str(prod.id)] = {
#             "producto_id": prod.id,
#             "nombre": prod.nombre,
#             "precio_unit": prod.precio_unit,
#             "precio_media": prod.precio_media,
#             "precio_doc": prod.precio_doc,
#             "cantidad": float(producto.cantidad),
#             "subtotal": float(producto.subtotal),
#             "categoria": prod.categoria.nombre
#         }

#     return pedidos