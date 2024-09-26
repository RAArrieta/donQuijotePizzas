import calendar
from datetime import timedelta, date
from django.utils import timezone
from facturas.models import FacturaProducto
from productos.models import Producto, ProductoCategoria
from django.db.models import Sum, Min, Max, Avg, Count

class Estadisticas:
    def __init__(self, producto_id,  producto_nombre, categoria, cantidad_vendida, cantidad_promedio, fecha_inicio, fecha_fin, dia_semana, media_semana, mes, ano, cantidad_dias):
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.categoria= categoria
        self.cantidad_vendida = cantidad_vendida
        self.cantidad_promedio = cantidad_promedio
        # self.cantidad_minima = cantidad_minima
        # self.cantidad_maxima = cantidad_maxima
        # self.cantidad_no_vendida = cantidad_no_vendida
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.dia_semana = dia_semana
        self.media_semana = media_semana
        self.mes = mes
        self.ano = ano
        self.cantidad_dias = cantidad_dias
        
    def calcular_cantidad_vendida(self):
            try:
                productos_vendidos = Estadisticas.productos_vendidos(self)
                self.cantidad_vendida = productos_vendidos.aggregate(total_vendido=Sum('cantidad'))['total_vendido'] or 0  
                Estadisticas.calcular_cantidad_dias(self, productos_vendidos)
                if self.cantidad_dias > 0 and self.cantidad_vendida > 0:
                    self.cantidad_promedio = round(self.cantidad_vendida / self.cantidad_dias, 1)
                else:
                    self.cantidad_promedio = 0
            except Producto.DoesNotExist:
                print(f"Producto {self.producto_nombre} no existe.")
                
    def productos_vendidos(self):
        if self.producto_id:
            producto_seleccionado = Producto.objects.get(id=self.producto_id) 
            fecha_actual = timezone.now()
            fecha_inicio = fecha_actual - timedelta(days=85)
            productos_vendidos = FacturaProducto.objects.filter(
                producto=producto_seleccionado,
                factura__fecha__range=(fecha_inicio, fecha_actual)
            )
            if self.fecha_inicio and self.fecha_fin:
                productos_vendidos = productos_vendidos.filter(
                    factura__fecha__range=[self.fecha_inicio, self.fecha_fin]
                )
            if self.dia_semana:
                productos_vendidos = productos_vendidos.filter(
                    factura__fecha__week_day=int(self.dia_semana)
                )  
            if self.media_semana:
                if self.media_semana == "m_j":
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__week_day__in=[3, 4, 5]
                    )
                else:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__week_day__in=[6, 7, 1]
                    )
            if self.mes and self.ano:
                if self.mes != "0":
                    mes = int(self.mes)
                    ano = int(self.ano)
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__month=mes,
                        factura__fecha__year=ano
                    ) 
                else:
                    ano = int(self.ano)
                    productos_vendidos = productos_vendidos.filter(factura__fecha__year=ano) 
                    
        elif self.categoria:
            productos_categoria = Producto.objects.filter(categoria__nombre=self.categoria)
            fecha_actual = timezone.now()
            fecha_inicio = fecha_actual - timedelta(days=85)
            productos_vendidos = FacturaProducto.objects.filter(
                producto__in=productos_categoria,
                factura__fecha__range=(fecha_inicio, fecha_actual)
            )
            if self.fecha_inicio and self.fecha_fin:
                productos_vendidos = productos_vendidos.filter(
                    factura__fecha__range=[self.fecha_inicio, self.fecha_fin]
                )
            if self.dia_semana:
                productos_vendidos = productos_vendidos.filter(
                    factura__fecha__week_day=int(self.dia_semana)
                )  
            if self.media_semana:
                if self.media_semana == "m_j":
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__week_day__in=[3, 4, 5]
                    )
                else:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__week_day__in=[6, 7, 1]
                    )
            if self.mes and self.ano:
                if self.mes != "0":
                    mes = int(self.mes)
                    ano = int(self.ano)
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__month=mes,
                        factura__fecha__year=ano
                    ) 
                else:
                    ano = int(self.ano)
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__year=ano
                    )               
        return productos_vendidos
               
    def calcular_cantidad_dias(self, productos_vendidos):
        if self.fecha_inicio and self.fecha_fin:
            self.cantidad_dias = (self.fecha_fin - self.fecha_inicio).days + 1           
        elif self.dia_semana:
            try:
                if productos_vendidos.exists():
                    primera_fecha = productos_vendidos.earliest('factura__fecha').factura.fecha
                    ultima_fecha = date.today()
                    dia_semana_deseado = int(self.dia_semana) - 2
                    cantidad_dias_semana = 0
                    fecha_actual = primera_fecha
                    
                    while fecha_actual <= ultima_fecha:
                        if fecha_actual.weekday() == dia_semana_deseado:  
                            cantidad_dias_semana += 1
                        fecha_actual += timedelta(days=1)  
                        
                    self.cantidad_dias = cantidad_dias_semana                    
                else:
                    self.cantidad_dias = 0
            except Producto.DoesNotExist:
                print(f"Producto {self.producto_nombre} no existe.")
            except ProductoCategoria.DoesNotExist:
                print(f"Categoría {self.categoria} no existe.")
        elif self.media_semana:
            try:
                if productos_vendidos.exists():
                    primera_fecha = productos_vendidos.earliest('factura__fecha').factura.fecha
                    ultima_fecha = date.today()
                    cantidad_dias_semana = 0
                    fecha_actual = primera_fecha
                    
                    if self.media_semana == "m_j":
                        while fecha_actual <= ultima_fecha:
                            if fecha_actual.weekday() in [1, 2, 3]: 
                                cantidad_dias_semana += 1
                            fecha_actual += timedelta(days=1)
                            
                        self.cantidad_dias = cantidad_dias_semana
                    else:
                        while fecha_actual <= ultima_fecha:
                            if fecha_actual.weekday() in [4, 5, 6]:  
                                cantidad_dias_semana += 1
                            fecha_actual += timedelta(days=1)
                            
                        self.cantidad_dias = cantidad_dias_semana
                else:
                    self.cantidad_dias = 0
            except Producto.DoesNotExist:
                print(f"Producto {self.producto_nombre} no existe.")
            except ProductoCategoria.DoesNotExist:
                print(f"Categoría {self.categoria} no existe.")
        elif self.mes and self.ano:
            if self.mes != "0":
                mes = int(self.mes)
                ano = int(self.ano)
                print(f"mes: {mes}")
                _, self.cantidad_dias = calendar.monthrange(ano, mes)
            else:
                self.cantidad_dias = 365
                
        else:
            self.cantidad_dias = 0

                   
    def calcular_minimo():
        pass

    def calcular_maximo():
        pass

    def calcular_promedio():
        pass

    def calcular_no_vendidos():
        pass