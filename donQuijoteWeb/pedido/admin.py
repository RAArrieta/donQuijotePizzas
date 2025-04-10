from django.contrib import admin
from .models import Pedido, PedidoProductos, FormaEntrega, PedidosReservado, PedidosProductosReservados

admin.site.register([Pedido, PedidoProductos, FormaEntrega, PedidosReservado, PedidosProductosReservados])