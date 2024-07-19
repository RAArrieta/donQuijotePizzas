from django.contrib import admin
from .models import Pedido, PedidoProductos, FormaEntrega

admin.site.register([Pedido, PedidoProductos, FormaEntrega])