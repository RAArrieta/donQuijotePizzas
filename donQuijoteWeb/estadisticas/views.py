from django.shortcuts import render
from django.db import models


from carro.select_productos import select_productos
from productos.models import Producto, ProductoCategoria
from facturas.models import FacturaProducto

# def home(request):
#     categorias=select_productos()
#     productos_vendidos= FacturaProducto.objects.all() # ESTOS SON LOS PRODUCTOS VENDIDOS

#     producto_seleccionado = None
#     categoria_seleccionada = None

#     if request.method == 'POST':
#         producto_id = request.POST.get('producto_id')
#         categoria_id = request.POST.get('categoria_id')
        
#         if producto_id:
#             try:
#                 producto_seleccionado = Producto.objects.get(id=producto_id) #AQUI SELECCIONE UN PRODUCTO Y QUIERO SABER CUANTOS SE VENDIERON

#             except Producto.DoesNotExist:
#                 producto_seleccionado = None
        
#         if categoria_id:
#             categoria_seleccionada = categoria_id
            
    
#     context = {
#         'categorias': categorias,
#         'producto_seleccionado':producto_seleccionado,
#         'categoria_seleccionada':categoria_seleccionada,
#         'productos_vendidos':productos_vendidos,

#     }
#     return render(request, "estadisticas/index.html", context)
# def home(request):
#     categorias = select_productos()
#     productos_vendidos = FacturaProducto.objects.all()  # Todos los productos vendidos
    
#     producto_seleccionado = None
#     categoria_seleccionada = None
#     cantidad_vendida = 0  # Inicializamos la cantidad vendida a 0

#     if request.method == 'POST':
#         producto_id = request.POST.get('producto_id')
#         categoria_id = request.POST.get('categoria_id')
        
#         if producto_id:
#             try:
#                 producto_seleccionado = Producto.objects.get(id=producto_id)  # Producto seleccionado
                
#                 # Filtrar los productos vendidos del producto seleccionado y sumar las cantidades
#                 cantidad_vendida = FacturaProducto.objects.filter(producto=producto_seleccionado).aggregate(total_vendido=models.Sum('cantidad'))['total_vendido'] or 0
                
#             except Producto.DoesNotExist:
#                 producto_seleccionado = None
        
#         if categoria_id:
#             categoria_seleccionada = categoria_id
#             try:
#                 # Filtrar los productos de la categoría seleccionada
#                 productos_categoria = Producto.objects.filter(categoria_id=categoria_id)
                
#                 # Filtrar los productos vendidos que pertenecen a la categoría seleccionada y sumar las cantidades
#                 cantidad_vendida = FacturaProducto.objects.filter(producto__in=productos_categoria).aggregate(total_vendido=models.Sum('cantidad'))['total_vendido'] or 0
                
#             except ProductoCategoria.DoesNotExist:
#                 categoria_seleccionada = None
#     context = {
#         'categorias': categorias,
#         'producto_seleccionado': producto_seleccionado,
#         'categoria_seleccionada': categoria_seleccionada,
#         'productos_vendidos': productos_vendidos,
#         'cantidad_vendida': cantidad_vendida,  # Agregamos la cantidad vendida al contexto
#     }
    
#     return render(request, "estadisticas/index.html", context)









from django.shortcuts import render
from django.db import models
from productos.models import Producto, ProductoCategoria  # Asegúrate de importar el modelo ProductoCategoria
from facturas.models import FacturaProducto

from django.shortcuts import render
from django.db import models
from .models import Producto, FacturaProducto, ProductoCategoria

def home(request):
    categorias = ProductoCategoria.objects.all()  # Obtener todas las categorías
    productos_vendidos = FacturaProducto.objects.all()  # Todos los productos vendidos
    
    producto_seleccionado = None
    categoria_seleccionada = None
    cantidad_vendida = 0  # Inicializamos la cantidad vendida a 0

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        categoria_nombre = request.POST.get('categoria_id')  # Cambiado a categoria_nombre
        
        if producto_id:
            try:
                producto_seleccionado = Producto.objects.get(id=producto_id)  # Producto seleccionado
                
                # Filtrar los productos vendidos del producto seleccionado y sumar las cantidades
                cantidad_vendida = FacturaProducto.objects.filter(producto=producto_seleccionado).aggregate(total_vendido=models.Sum('cantidad'))['total_vendido'] or 0
                
            except Producto.DoesNotExist:
                producto_seleccionado = None
        
        if categoria_nombre:
            try:
                categoria_seleccionada = ProductoCategoria.objects.get(nombre=categoria_nombre)  # Obtén la categoría por nombre
                print(categoria_seleccionada)
                
                # Filtrar los productos de la categoría seleccionada
                productos_categoria = Producto.objects.filter(categoria=categoria_seleccionada)
                
                # Filtrar los productos vendidos que pertenecen a la categoría seleccionada y sumar las cantidades
                cantidad_vendida = FacturaProducto.objects.filter(producto__in=productos_categoria).aggregate(total_vendido=models.Sum('cantidad'))['total_vendido'] or 0
                
            except ProductoCategoria.DoesNotExist:
                categoria_seleccionada = None
    
    context = {
        'categorias': categorias,
        'producto_seleccionado': producto_seleccionado,
        'categoria_seleccionada': categoria_seleccionada,
        'productos_vendidos': productos_vendidos,
        'cantidad_vendida': cantidad_vendida,  # Agregamos la cantidad vendida al contexto
    }
    
    return render(request, "estadisticas/index.html", context)
