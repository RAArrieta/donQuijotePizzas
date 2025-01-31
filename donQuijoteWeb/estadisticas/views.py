from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date
from carro.select_productos import select_productos
from .estadisticas import Estadisticas
from productos.models import Producto
from .forms import MesAnoForm

def home(request):
    categorias = select_productos()
    estadisticas = request.session.get('estadisticas', None)
    form = MesAnoForm(request.POST or None)

    dias_semana = {
        '0': 'Hoy',
        '1': 'Domingo',
        '3': 'Martes',
        '4': 'Miércoles',
        '5': 'Jueves',
        '6': 'Viernes',
        '7': 'Sábado',
    }
    
    mes = {
        '0': 'Todo el año',
        '1': 'Enero',
        '2': 'Febrero',
        '3': 'Marzo',
        '4': 'Abril',
        '5': 'Mayo',
        '6': 'Junio',
        '7': 'Julio',
        '8': 'Agosto',
        '9': 'Septiembre',
        '10': 'Octubre',
        '11': 'Noviembre',
        '12': 'Diciembre',  
    }

    dia_semana_nombre = dias_semana.get(str(estadisticas.get('dia_semana', '')), '') if estadisticas else ''
    mes_nombre = mes.get(str(estadisticas.get('mes', '')), '') if estadisticas else ''
 
    context = {
        'categorias': categorias,
        'estadisticas': estadisticas,  
        'form': form,
        'dia_semana_nombre': dia_semana_nombre,
        'mes_nombre': mes_nombre,
    }
    
    return render(request, "estadisticas/index.html", context)

def cargar_datos(request):
    if request.method == 'POST':    
        categoria = request.POST.get('categoria', None)         
        producto_id = request.POST.get('producto_id', None)
        
        if producto_id:
            try:
                producto = Producto.objects.get(id=producto_id)
                producto_nombre = producto.nombre
                categoria = request.POST.get('categoria', producto.categoria.nombre)  
            except Producto.DoesNotExist:
                producto_nombre = None
                categoria = None
        else:
            producto_nombre = None
            categoria = request.POST.get('categoria', None)
            
            
            
        # if producto_id:
        #     try:
        #         producto_nombre = Producto.objects.get(id=producto_id).nombre
        #     except Producto.DoesNotExist:
        #         producto_nombre = None
        # else:
        #     producto_nombre = None
            
            
        envios = request.POST.get('envios', None)
        fecha_inicio = request.POST.get("fecha_inicio", None)
        fecha_fin = request.POST.get("fecha_fin", None)
        fecha_inicio = parse_date(fecha_inicio) if fecha_inicio else None
        fecha_fin = parse_date(fecha_fin) if fecha_fin else None
        dia_semana = request.POST.get("dia_semana", None)
        media_semana = request.POST.get("media_semana", None)
        mes = request.POST.get("mes", None)
        ano = request.POST.get("ano", None)
              
        if producto_id or categoria or envios:
            estadisticas = Estadisticas(
                producto_id=producto_id,
                producto_nombre=producto_nombre,
                categoria=categoria,
                cantidad_vendida=0, 
                cantidad_promedio=0,
                cantidad_minima=0,
                cantidad_maxima=0,
                dia_venta=0,
                dia_no_venta=0,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                dia_semana=dia_semana,
                media_semana=media_semana,
                mes=mes if (fecha_inicio is None and dia_semana is None and media_semana is None) else None,
                ano=ano if (fecha_inicio is None and dia_semana is None and media_semana is None) else None,
                cantidad_dias=0
            )
            
            estadisticas.estadisticas() 
            
            request.session['estadisticas'] = {
                'producto_id': producto_id,
                'producto_nombre': producto_nombre,
                'categoria': categoria,
                'cantidad_vendida': estadisticas.cantidad_vendida, 
                'cantidad_promedio': estadisticas.cantidad_promedio,
                'cantidad_minima': estadisticas.cantidad_minima,
                'cantidad_maxima': estadisticas.cantidad_maxima,
                'dia_venta': estadisticas.dia_venta,
                'dia_no_venta': estadisticas.dia_no_venta,
                'fecha_inicio': str(estadisticas.fecha_inicio) if fecha_inicio else None,
                'fecha_fin': str(estadisticas.fecha_fin) if fecha_fin else None,
                'dia_semana': dia_semana,
                'media_semana': media_semana,
                'mes': mes if (fecha_inicio is None and dia_semana is None and mes and ano) else None,
                'ano': ano if (fecha_inicio is None and dia_semana is None and mes and ano) else None,
                'cantidad_dias': estadisticas.cantidad_dias,     
            }
        else:
            messages.warning(request, "Debe seleccionar un producto o categoría y filtrar una fecha...")
            
        
    
    return redirect('estadisticas:home')
# from django.contrib import messages
# from django.shortcuts import redirect, render
# from django.utils.dateparse import parse_date
# from carro.select_productos import select_productos
# from .estadisticas import Estadisticas
# from productos.models import Producto
# from .forms import MesAnoForm

# def home(request):
#     categorias = select_productos()
#     estadisticas = request.session.get('estadisticas', None)
#     form = MesAnoForm(request.POST or None)

#     dias_semana = {
#         '1': 'Domingo',
#         '3': 'Martes',
#         '4': 'Miércoles',
#         '5': 'Jueves',
#         '6': 'Viernes',
#         '7': 'Sábado',
#     }
    
#     mes = {
#         '0': 'Todo el año',
#         '1': 'Enero',
#         '2': 'Febrero',
#         '3': 'Marzo',
#         '4': 'Abril',
#         '5': 'Mayo',
#         '6': 'Junio',
#         '7': 'Julio',
#         '8': 'Agosto',
#         '9': 'Septiembre',
#         '10': 'Octubre',
#         '11': 'Noviembre',
#         '12': 'Diciembre',  
#     }

#     dia_semana_nombre = dias_semana.get(str(estadisticas.get('dia_semana', '')), '') if estadisticas else ''
#     mes_nombre = mes.get(str(estadisticas.get('mes', '')), '') if estadisticas else ''
 
#     context = {
#         'categorias': categorias,
#         'estadisticas': estadisticas,  
#         'form': form,
#         'dia_semana_nombre': dia_semana_nombre,
#         'mes_nombre': mes_nombre,
#     }
    
#     return render(request, "estadisticas/index.html", context)

# def cargar_datos(request):
#     if request.method == 'POST':    
#         categoria = request.POST.get('categoria', None)          
#         producto_id = request.POST.get('producto_id', None)
#         if producto_id:
#             try:
#                 producto_nombre = Producto.objects.get(id=producto_id).nombre
#             except Producto.DoesNotExist:
#                 producto_nombre = None
#         else:
#             producto_nombre = None
#         envios = request.POST.get('envios', None)
#         fecha_inicio = request.POST.get("fecha_inicio", None)
#         fecha_fin = request.POST.get("fecha_fin", None)
#         fecha_inicio = parse_date(fecha_inicio) if fecha_inicio else None
#         fecha_fin = parse_date(fecha_fin) if fecha_fin else None
#         dia_semana = request.POST.get("dia_semana", None)
#         media_semana = request.POST.get("media_semana", None)
#         mes = request.POST.get("mes", None)
#         ano = request.POST.get("ano", None)
              
#         if producto_id or categoria or envios:
#             estadisticas = Estadisticas(
#                 producto_id=producto_id,
#                 producto_nombre=producto_nombre,
#                 categoria=categoria,
#                 cantidad_vendida=0, 
#                 cantidad_promedio=0,
#                 cantidad_minima=0,
#                 cantidad_maxima=0,
#                 dia_venta=0,
#                 dia_no_venta=0,
#                 fecha_inicio=fecha_inicio,
#                 fecha_fin=fecha_fin,
#                 dia_semana=dia_semana,
#                 media_semana=media_semana,
#                 mes=mes if (fecha_inicio is None and dia_semana is None and media_semana is None) else None,
#                 ano=ano if (fecha_inicio is None and dia_semana is None and media_semana is None) else None,
#                 cantidad_dias=0
#             )
            
#             estadisticas.estadisticas() 
            
#             request.session['estadisticas'] = {
#                 'producto_id': producto_id,
#                 'producto_nombre': producto_nombre,
#                 'categoria': categoria,
#                 'cantidad_vendida': estadisticas.cantidad_vendida, 
#                 'cantidad_promedio': estadisticas.cantidad_promedio,
#                 'cantidad_minima': estadisticas.cantidad_minima,
#                 'cantidad_maxima': estadisticas.cantidad_maxima,
#                 'dia_venta': estadisticas.dia_venta,
#                 'dia_no_venta': estadisticas.dia_no_venta,
#                 'fecha_inicio': str(estadisticas.fecha_inicio) if fecha_inicio else None,
#                 'fecha_fin': str(estadisticas.fecha_fin) if fecha_fin else None,
#                 'dia_semana': dia_semana,
#                 'media_semana': media_semana,
#                 'mes': mes if (fecha_inicio is None and dia_semana is None and mes and ano) else None,
#                 'ano': ano if (fecha_inicio is None and dia_semana is None and mes and ano) else None,
#                 'cantidad_dias': estadisticas.cantidad_dias,     
#             }
#         else:
#             messages.warning(request, "Debe seleccionar un producto o categoría y filtrar una fecha...")
            
        
    
#     return redirect('estadisticas:home')