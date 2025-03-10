from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('productos/', include('productos.urls')),
    path('carro/', include('carro.urls')),
    path('pedido/', include('pedido.urls')),
    path('facturas/', include('facturas.urls')),
    path('estadisticas/', include('estadisticas.urls')),
    path('gastos/', include('gastos.urls')),
    path('contable/', include('contable.urls')),
]
