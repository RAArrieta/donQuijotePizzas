from django.contrib import admin
from .models import Pedido, PedidoProductos, FormaEntrega, Descuentos, PedidosReservado, PedidosProductosReservados

admin.site.register([Pedido, PedidoProductos, FormaEntrega, Descuentos, PedidosReservado, PedidosProductosReservados])