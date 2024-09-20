from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date
from carro.select_productos import select_productos
from .estadisticas import Estadisticas
from productos.models import Producto

def home(request):
    categorias = select_productos()
    estadisticas = request.session.get('estadisticas', None)
    
    context = {
        'categorias': categorias,
        'estadisticas': estadisticas,  
    }
    
    return render(request, "estadisticas/index.html", context)

def cargar_datos(request):
    if request.method == 'POST':              
        producto_id = request.POST.get('producto_id', None)
        if producto_id:
            try:
                producto_nombre = Producto.objects.get(id=producto_id).nombre
            except Producto.DoesNotExist:
                producto_nombre = None
        else:
            producto_nombre = None
        categoria = request.POST.get('categoria', None)
        fecha_inicio = request.POST.get("fecha_inicio", None)
        fecha_fin = request.POST.get("fecha_fin", None)
        dia_semana = request.POST.get("dia_semana", None)
        
        fecha_inicio = parse_date(fecha_inicio) if fecha_inicio else None
        fecha_fin = parse_date(fecha_fin) if fecha_fin else None
        
        if (producto_id or categoria) and (fecha_inicio or dia_semana):
            estadisticas = Estadisticas(
                producto_id=producto_id,
                producto_nombre=producto_nombre,
                categoria=categoria,
                cantidad_vendida=0, 
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                dia_semana=dia_semana,
                cantidad_dias=0
            )

            estadisticas.calcular_cantidad_vendida()
            estadisticas.calcular_cantidad_dias()

            request.session['estadisticas'] = {
                'producto_id': producto_id,
                'producto_nombre': producto_nombre,
                'categoria': categoria,
                'cantidad_vendida': estadisticas.cantidad_vendida, 
                'fecha_inicio': str(fecha_inicio) if fecha_inicio else None,
                'fecha_fin': str(fecha_fin) if fecha_fin else None,
                'dia_semana': dia_semana,
                'cantidad_dias': estadisticas.cantidad_dias,     
            }
        else:
            messages.warning(request, "Debe seleccionar un producto o categoria y filtrar una fecha...")
    
    return redirect('estadisticas:home')

# def home(request):
#     categorias = select_productos()
    
#     estadisticas = Estadisticas()
    
#     print(f"Producto Seleccionado: {estadisticas.producto_seleccionado}")
#     print(f"Categoría Seleccionada: {estadisticas.categoria_seleccionada}")
#     print(f"Fecha inicio: {estadisticas.fecha_inicio}")
#     print(f"Fecha Fin: {estadisticas.fecha_fin}")
#     print(f"Dia Seleccionado: {estadisticas.dia_semana}")
#     estadisticas = Estadisticas()
#     productos_vendidos = FacturaProducto.objects.all()

#     producto_seleccionado = None
#     categoria_seleccionada = None
#     cantidad_vendida = 0
#     cantidad_promedio = 0
#     cantidad_minima = 0
#     cantidad_maxima = 0
#     cantidad_no_vendida = 0



#         if producto_id:
#             try:
#                 producto_seleccionado = Producto.objects.get(id=producto_id)
                
#                 productos_vendidos = FacturaProducto.objects.filter(
#                     producto=producto_seleccionado
#                 )
#                 if fecha_inicio and fecha_fin:
#                     productos_vendidos = productos_vendidos.filter(
#                         factura__fecha__range=[fecha_inicio, fecha_fin]
#                     )
#                 if dia_semana:
#                     productos_vendidos = productos_vendidos.filter(
#                         factura__fecha__week_day=int(dia_semana)
#                     )
#                 cantidad_vendida = productos_vendidos.aggregate(total_vendido=Sum('cantidad'))['total_vendido'] or 0           
#             except Producto.DoesNotExist:
#                 producto_seleccionado = None
        
#         if categoria:
#             categoria_seleccionada = categoria
#             try:
#                 productos_categoria = Producto.objects.filter(categoria__nombre=categoria)
#                 productos_vendidos = FacturaProducto.objects.filter(
#                     producto__in=productos_categoria
#                 )
#                 if fecha_inicio and fecha_fin:
#                     productos_vendidos = productos_vendidos.filter(
#                         factura__fecha__range=[fecha_inicio, fecha_fin]
#                     )
#                     diferencia = fecha_fin - fecha_inicio
#                     cantidad_dias = diferencia.days + 1
#                     print(f"Canfidad de dias: {cantidad_dias}")
#                 if dia_semana:
#                     productos_vendidos = productos_vendidos.filter(
#                         factura__fecha__week_day=int(dia_semana)
#                     )

#                     # Obtener la fecha más antigua y más reciente de ventas los días miércoles.
#                     primera_fecha = productos_vendidos.earliest('factura__fecha').factura.fecha
#                     ultima_fecha = productos_vendidos.latest('factura__fecha').factura.fecha
#                     print(f"Primera fecha: {primera_fecha}, Ultima fecha: {ultima_fecha}")

#                     # Calcular la cantidad de días de la semana (miércoles) entre la primera y la última fecha
#                     dias_totales = (ultima_fecha - primera_fecha).days
#                     print(f"Dias totales: {dias_totales}")

#                     # Verificar si la primera y última fecha son iguales
#                     if primera_fecha == ultima_fecha:
#                         # Si las fechas son iguales, hay al menos un día válido.
#                         cantidad_dias = 1 # if primera_fecha.weekday() == int(dia_semana) - 1 else 0 'TUVE QUE COMENTAR ESTE IF PORQUE ME DEVUELVE 0'
#                     else:
#                         # Si hay más de un día en el rango, contar los días específicos.
#                         cantidad_dias = sum(1 for i in range(dias_totales + 1)
#                                             if (primera_fecha + timedelta(days=i)).weekday() == int(dia_semana) - 1)

#                     print(f"Cantidad de dias: {cantidad_dias}")

                    
                    
                    
#                 cantidad_vendida = productos_vendidos.aggregate(total_vendido=Sum('cantidad'))['total_vendido'] or 0
#             except ProductoCategoria.DoesNotExist:
#                 categoria_seleccionada = None
                
#     context = {
#         'categorias': categorias,
#         'producto_seleccionado': producto_seleccionado,
#         'categoria_seleccionada': categoria_seleccionada,
#         'productos_vendidos': productos_vendidos,
#         'cantidad_vendida': cantidad_vendida,
#         'cantidad_promedio': cantidad_promedio,
#         'cantidad_minima': cantidad_minima,
#         'cantidad_maxima': cantidad_maxima,
#         'cantidad_no_vendida': cantidad_no_vendida,
#     }
    
#     return render(request, "estadisticas/index.html", context)