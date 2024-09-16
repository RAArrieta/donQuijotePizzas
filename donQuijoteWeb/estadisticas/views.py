from django.shortcuts import render
from django.db import models
from django.db.models.functions import ExtractWeekDay
from django.utils.dateparse import parse_date
from carro.select_productos import select_productos
from productos.models import Producto, ProductoCategoria
from facturas.models import FacturaProducto

def home(request):
    categorias = select_productos()
    productos_vendidos = FacturaProducto.objects.all()
    
    producto_seleccionado = None
    categoria_seleccionada = None
    cantidad_vendida = 0

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        categoria = request.POST.get('categoria')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        dia_semana = request.POST.get('dia_semana')  
        print(f"Dia seleccionado: {dia_semana}")

        fecha_inicio = parse_date(fecha_inicio) if fecha_inicio else None
        fecha_fin = parse_date(fecha_fin) if fecha_fin else None

        if producto_id:
            try:
                producto_seleccionado = Producto.objects.get(id=producto_id)
                
                # Aplicar filtro por fechas si están disponibles
                productos_vendidos = FacturaProducto.objects.filter(
                    producto=producto_seleccionado
                )
                if fecha_inicio and fecha_fin:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__range=[fecha_inicio, fecha_fin]
                    )
                if dia_semana:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__week_day=int(dia_semana)
                    )
                cantidad_vendida = productos_vendidos.aggregate(total_vendido=models.Sum('cantidad'))['total_vendido'] or 0           
                print(f"Producto: {producto_seleccionado}")   
            except Producto.DoesNotExist:
                producto_seleccionado = None
        
        if categoria:
            categoria_seleccionada = categoria
            try:
                productos_categoria = Producto.objects.filter(categoria__nombre=categoria)
                productos_vendidos = FacturaProducto.objects.filter(
                    producto__in=productos_categoria
                )
                if fecha_inicio and fecha_fin:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__range=[fecha_inicio, fecha_fin]
                    )
                if dia_semana:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__week_day=int(dia_semana)
                    )
                cantidad_vendida = productos_vendidos.aggregate(total_vendido=models.Sum('cantidad'))['total_vendido'] or 0
                print(f"Cantidad vendida de {productos_categoria}: {cantidad_vendida}")
            except ProductoCategoria.DoesNotExist:
                categoria_seleccionada = None
                
    context = {
        'categorias': categorias,
        'producto_seleccionado': producto_seleccionado,
        'categoria_seleccionada': categoria_seleccionada,
        'productos_vendidos': productos_vendidos,
        'cantidad_vendida': cantidad_vendida,
    }
    
    return render(request, "estadisticas/index.html", context)

