from django.contrib import admin
from .models import Pedido, PedidoProductos

# Register your models here.

admin.site.register([Pedido, PedidoProductos])