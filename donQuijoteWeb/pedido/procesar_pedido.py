
from django.contrib import messages

# from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from pedido.models import FormaEntrega, Pedido, PedidoProductos, PedidosReservado, PedidosProductosReservados
from carro.carro import Carro
from pedido.recuperar_pedidos import recuperar_pedidos

from productos.models import Producto
from django.db import transaction

# @transaction.atomic
# def procesar_pedido(request):
#     nro_pedido = request.session.pop("nro_pedido", None)
#     carro = Carro(request)

#     pedido = None
#     es_reservado = False
#     datos_pedido = None
#     datos_empanadas = None
#     lista_productos = []

#     # ==============================
#     # 1️⃣ BUSCAR PEDIDO EXISTENTE
#     # ==============================
#     if nro_pedido:
#         pedido = Pedido.objects.filter(id=nro_pedido).first()
#         if not pedido:
#             pedido = PedidosReservado.objects.filter(id=nro_pedido).first()
#             if pedido:
#                 es_reservado = True

#     # ==============================
#     # 2️⃣ DECIDIR SI CHEQUEAR STOCK
#     # ==============================
#     if es_reservado:
#         chequear_stock = False
#     else:
#         chequear_stock = productos_modificados(pedido, carro, es_reservado)

#     if chequear_stock:
#         ok, faltantes = recheq_stock_pedido(request, pedido)
#         if not ok:
#             for prod, stock in faltantes.items():
#                 messages.error(
#                     request,
#                     f"{prod}: stock disponible {stock}"
#                 )
#             return redirect("carro:carro")

#     # ==============================
#     # 3️⃣ LEER CARRITO (SIN DB)
#     # ==============================
#     for key, value in carro.carro.items():

#         # -------- productos --------
#         if key not in ["datos", "empanadas"]:
#             modelo_producto = (
#                 PedidosProductosReservados if es_reservado else PedidoProductos
#             )
#             lista_productos.append(
#                 modelo_producto(
#                     producto_id=key,
#                     cantidad=value["cantidad"],
#                     subtotal=value["subtotal"],
#                 )
#             )

#         # -------- datos del pedido --------
#         elif key == "datos":
#             forma_entrega_obj = get_object_or_404(
#                 FormaEntrega,
#                 forma_entrega=value["forma_entrega"]
#             )

#             datos_pedido = {
#                 "estado": value["estado"],
#                 "pago": value["pago"],
#                 "forma_entrega": forma_entrega_obj,
#                 "precio_entrega": value["precio_entrega"],
#                 "nombre": value["nombre"],
#                 "direccion": value["direccion"],
#                 "observacion": value["observacion"],
#                 "total": value["total"],
#             }

#             if value["estado"].lower() == "reservado":
#                 es_reservado = True

#         # -------- empanadas --------
#         elif key == "empanadas":
#             datos_empanadas = {
#                 "cantidad": value["cantidad"],
#                 "subtotal": value["subtotal_emp"],
#             }

#     # ==============================
#     # 4️⃣ CREAR O ACTUALIZAR PEDIDO
#     # ==============================
#     modelo_pedido = PedidosReservado if es_reservado else Pedido

#     if pedido:
#         # editar pedido existente
#         for campo, valor in datos_pedido.items():
#             setattr(pedido, campo, valor)
#         pedido.save()
#     else:
#         # pedido nuevo → acá nace el nro de pedido
#         pedido = modelo_pedido.objects.create(**datos_pedido)

#     # ==============================
#     # 5️⃣ EMPANADAS
#     # ==============================
#     if datos_empanadas:
#         pedido.cantidad_emp = datos_empanadas["cantidad"]
#         pedido.subtotal_emp = datos_empanadas["subtotal"]
#         pedido.save()

#     # ==============================
#     # 6️⃣ PRODUCTOS Y STOCK
#     # ==============================
#     modelo_producto = (
#         PedidosProductosReservados if es_reservado else PedidoProductos
#     )

#     productos_previos = modelo_producto.objects.filter(pedido=pedido)

#     if chequear_stock:
#         # devolver stock previo
#         for item in productos_previos:
#             producto = item.producto
#             categoria = producto.categoria
#             producto.cantidad += item.cantidad
#             categoria.cantidad += item.cantidad
#             producto.save()
#             categoria.save()

#         productos_previos.delete()

#     # asignar pedido a productos nuevos
#     for item in lista_productos:
#         item.pedido = pedido

#     modelo_producto.objects.bulk_create(lista_productos)

#     # descontar stock nuevo
#     if chequear_stock:
#         for item in lista_productos:
#             producto = item.producto
#             categoria = producto.categoria
#             producto.cantidad -= item.cantidad
#             categoria.cantidad -= item.cantidad
#             producto.save()
#             categoria.save()

#     # ==============================
#     # 7️⃣ LIMPIAR Y REDIRIGIR
#     # ==============================
#     carro.limpiar_carro()
#     return redirect("pedido:listar_pendientes")
@transaction.atomic
def procesar_pedido(request):
    nro_pedido = request.session.pop("nro_pedido", None)
    carro = Carro(request)

    pedido = None
    es_reservado = False
    datos_pedido = {}
    datos_empanadas = None
    lista_productos = []

    # ==============================
    # 1️⃣ BUSCAR PEDIDO EXISTENTE
    # ==============================
    if nro_pedido:
        pedido = Pedido.objects.filter(id=nro_pedido).first()
        if not pedido:
            pedido = PedidosReservado.objects.filter(id=nro_pedido).first()
            if pedido:
                es_reservado = True

    estado_anterior = pedido.estado.lower() if pedido else None

    # ==============================
    # 2️⃣ LEER CARRITO COMPLETO
    # ==============================
    for key, value in carro.carro.items():

        # -------- productos --------
        if key not in ["datos", "empanadas"]:
            lista_productos.append({
                "producto_id": int(key),
                "cantidad": float(value["cantidad"]),
                "subtotal": value["subtotal"],
            })

        # -------- datos del pedido --------
        elif key == "datos":
            forma_entrega_obj = get_object_or_404(
                FormaEntrega,
                forma_entrega=value["forma_entrega"]
            )

            datos_pedido = {
                "estado": value["estado"],
                "pago": value["pago"],
                "forma_entrega": forma_entrega_obj,
                "precio_entrega": value["precio_entrega"],
                "nombre": value["nombre"],
                "direccion": value["direccion"],
                "observacion": value["observacion"],
                "total": value["total"],
            }

            if value["estado"].lower() == "reservado":
                es_reservado = True

        # -------- empanadas --------
        elif key == "empanadas":
            datos_empanadas = {
                "cantidad": value["cantidad"],
                "subtotal": value["subtotal_emp"],
            }

    estado_nuevo = datos_pedido.get("estado", "").lower()

    # ==============================
    # 3️⃣ DETECTAR CANCELACIÓN
    # ==============================
    es_cancelado = (
        pedido
        and not es_reservado
        and estado_nuevo == "cancelado"
        and estado_anterior != "cancelado"
    )

    # ==============================
    # 4️⃣ DECIDIR STOCK
    # ==============================
    if es_reservado or es_cancelado:
        chequear_stock = False
    else:
        chequear_stock = productos_modificados(pedido, carro, es_reservado)

    if chequear_stock:
        ok, faltantes = recheq_stock_pedido(request, pedido)
        if not ok:
            for prod, stock in faltantes.items():
                messages.error(
                    request,
                    f"{prod}: stock disponible {stock}"
                )
            return redirect("carro:carro")

    # ==============================
    # 5️⃣ CREAR O ACTUALIZAR PEDIDO
    # ==============================
    modelo_pedido = PedidosReservado if es_reservado else Pedido

    if pedido:
        for campo, valor in datos_pedido.items():
            setattr(pedido, campo, valor)
        pedido.save()
    else:
        pedido = modelo_pedido.objects.create(**datos_pedido)

    # ==============================
    # 6️⃣ EMPANADAS
    # ==============================
    if datos_empanadas:
        pedido.cantidad_emp = datos_empanadas["cantidad"]
        pedido.subtotal_emp = datos_empanadas["subtotal"]
        pedido.save()

    # ==============================
    # 7️⃣ DEVOLVER STOCK SI SE CANCELA
    # ==============================
    if es_cancelado:
        productos_previos = PedidoProductos.objects.filter(pedido=pedido)

        for item in productos_previos:
            producto = item.producto
            categoria = producto.categoria
            producto.cantidad += item.cantidad
            categoria.cantidad += item.cantidad
            producto.save()
            categoria.save()

        productos_previos.delete()

        carro.limpiar_carro()
        return redirect("pedido:listar_pendientes")

    # ==============================
    # 8️⃣ PRODUCTOS Y STOCK NORMAL
    # ==============================
    modelo_producto = (
        PedidosProductosReservados if es_reservado else PedidoProductos
    )

    productos_previos = modelo_producto.objects.filter(pedido=pedido)

    if chequear_stock:
        for item in productos_previos:
            producto = item.producto
            categoria = producto.categoria
            producto.cantidad += item.cantidad
            categoria.cantidad += item.cantidad
            producto.save()
            categoria.save()

    productos_previos.delete()

    nuevos_items = [
        modelo_producto(
            pedido=pedido,
            producto_id=item["producto_id"],
            cantidad=item["cantidad"],
            subtotal=item["subtotal"],
        )
        for item in lista_productos
    ]

    modelo_producto.objects.bulk_create(nuevos_items)

    if chequear_stock:
        for item in nuevos_items:
            producto = item.producto
            categoria = producto.categoria
            producto.cantidad -= item.cantidad
            categoria.cantidad -= item.cantidad
            producto.save()
            categoria.save()

    # ==============================
    # 9️⃣ LIMPIAR Y REDIRIGIR
    # ==============================
    carro.limpiar_carro()
    return redirect("pedido:listar_pendientes")

def productos_modificados(pedido, carro, es_reservado):
    if es_reservado:
        return False

    if not pedido:
        return True

    modelo = PedidosProductosReservados if es_reservado else PedidoProductos

    productos_db = {
        (p.producto_id, float(p.cantidad))
        for p in modelo.objects.filter(pedido=pedido)
    }

    productos_carro = {
        (int(k), float(v["cantidad"]))
        for k, v in carro.carro.items()
        if k not in ["datos", "empanadas"]
    }

    return productos_db != productos_carro
   
def mod_pedido(request, tipo, pedido):
    nro_pedido_actual = request.session.get('nro_pedido')  
    nro_pedido_nuevo = pedido 

    if nro_pedido_actual is not None and str(nro_pedido_actual) != str(nro_pedido_nuevo):
        return redirect(reverse("pedido:modificar_pedido", args=[tipo, nro_pedido_actual]))

    datos_pedidos = recuperar_pedidos()  
    if tipo == "normal":
        pedidos = datos_pedidos.get("pedidos", {})
    else:  
        pedidos = datos_pedidos.get("pedidos_reservados", {})

    
    pedido = pedidos.get(nro_pedido_nuevo)
    if not pedido:
        messages.error(request, "El pedido no existe.")
        return redirect(reverse("pedido:home"))

    carro = Carro(request)
    carro.cargar_pedido(pedido)

    request.session['nro_pedido'] = nro_pedido_nuevo
    request.session['tipo_pedido'] = tipo
    
    
def recheq_stock_pedido(request, pedido=None):
    carro = Carro(request)
    faltantes = {}

    for key, value in carro.carro.items():
        if key in ["datos", "empanadas"]:
            continue

        producto = Producto.objects.get(id=key)
        cantidad_nueva = float(value.get("cantidad", 0))

        cantidad_anterior = 0
        if pedido:
            item = PedidoProductos.objects.filter(
                pedido=pedido,
                producto_id=key
            ).first()
            if item:
                cantidad_anterior = float(item.cantidad)

        diferencia = cantidad_nueva - cantidad_anterior

        # 🔥 SOLO si aumenta la cantidad
        if diferencia > 0 and diferencia > producto.cantidad:
            faltantes[producto.nombre] = producto.cantidad

    if faltantes:
        return False, faltantes

    return True, {}






























