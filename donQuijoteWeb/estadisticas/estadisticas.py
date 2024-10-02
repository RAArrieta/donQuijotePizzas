import calendar
from datetime import timedelta, date
from django.utils import timezone
from facturas.models import FacturaProducto
from productos.models import Producto, ProductoCategoria
from django.db.models import Sum, Min, Max, Avg, Count

class Estadisticas:
    def __init__(self, producto_id,  producto_nombre, categoria, cantidad_vendida, cantidad_promedio, dia_venta, dia_no_venta, fecha_inicio, fecha_fin, dia_semana, media_semana, mes, ano, cantidad_dias):
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.categoria= categoria
        self.cantidad_vendida = cantidad_vendida
        self.cantidad_promedio = cantidad_promedio
        # self.cantidad_minima = cantidad_minima
        # self.cantidad_maxima = cantidad_maxima
        self.dia_venta = dia_venta
        self.dia_no_venta = dia_no_venta
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.dia_semana = dia_semana
        self.media_semana = media_semana
        self.mes = mes
        self.ano = ano
        self.cantidad_dias = cantidad_dias
        
    def calcular_estadisticas(self):
            try:
                rango_facturado = Estadisticas.calculo_rango_facturado(self)
                print(f"RANGO FACTURADO: {rango_facturado}, tipo {type(rango_facturado)}")
                # productos_vendidos = Estadisticas.productos_vendidos(self)
                # Estadisticas.calcular_cantidad_vendida(self, productos_vendidos)
                # Estadisticas.calcular_cantidad_dias(self, productos_vendidos)
                # Estadisticas.calcular_dia_venta(self, productos_vendidos)
                
                # if self.cantidad_dias > 0 and self.cantidad_vendida > 0:
                #     if self.media_semana:
                #         self.cantidad_promedio = round((self.cantidad_vendida / self.cantidad_dias) * 3, 1)
                #     else:    
                #         self.cantidad_promedio = round(self.cantidad_vendida / self.cantidad_dias, 1)
                # else:
                #     self.cantidad_promedio = 0
                    
            except Producto.DoesNotExist:
                print(f"Producto {self.producto_nombre} no existe.")
                
    def calculo_rango_facturado(self):
        #Traigo todas las facturas
        total_facturas = FacturaProducto.objects.all()
        
        if total_facturas.exists():
            #Consigo la ultima fecha de facturacion y la convierto en el ultimo lunes
            ultima_factura = total_facturas.order_by('-factura__fecha').first()
            print(f"ULTIMO FACTURA: {ultima_factura}")
            ultima_fecha = ultima_factura.factura.fecha if ultima_factura else timezone.now()
            print(f"ULTIMA FECHA: {ultima_fecha}")
            ultima_fecha_for = ultima_fecha.weekday()   
            print(f"ULTIMO FECHA FOR: {ultima_fecha_for}") 
            if ultima_fecha_for != 0:
                ultima_fecha = ultima_fecha - timedelta(days=ultima_fecha_for)
            print(f"ULTIMO FECHA: {ultima_fecha}")
               
            #Consigo la primer fecha de facturacion y la convierto en el primer lunes 
            primera_factura = total_facturas.order_by('factura__fecha').first()
            print(f"PRIMER FACTURA: {primera_factura}")
            primer_fecha = primera_factura.factura.fecha if primera_factura else ultima_fecha - timedelta(days=92)
            print(f"PRIMER FECHA: {primer_fecha}")
            primer_fecha_for = primer_fecha.weekday()
            print(f"PRIMER FECHA_FOR {primer_fecha_for}")
            if primer_fecha_for != 0:
                primer_fecha = primer_fecha + timedelta(days=7-primer_fecha_for)
            print(f"PRIMER FECHA: {primer_fecha}")
                
            dif_fecha = (ultima_fecha - primer_fecha).days
            print(f"DIFERENCIA DE FECHA: {dif_fecha}")
                                
            if dif_fecha > 93:
                primer_fecha = ultima_fecha - timedelta(days=93)
                primer_fecha_for = primer_fecha.weekday()
                if primer_fecha_for != 0:
                    primer_fecha = primer_fecha + timedelta(days=7-primer_fecha_for) 
                    dif_fecha = (ultima_fecha - primer_fecha).days  
                    print(f"PRIMER FECHA MAYOR A 93: {primer_fecha}")     
                    
            if self.fecha_inicio and self.fecha_fin:
                if self.fecha_inicio < primer_fecha:
                    self.fecha_inicio = primer_fecha
                if self.fecha_fin > ultima_fecha:
                    self.fecha_fin = ultima_fecha
            
                    
            print(f"self.fecha_inicio: {self.fecha_inicio}")
            print(f"self.fecha_fin: {self.fecha_fin}")

            return {'primer_fecha': primer_fecha, 'ultima_fecha': ultima_fecha}
                    
            # productos_vendidos = total_facturas.filter(factura__fecha__range=(primer_lunes, ultimo_lunes))
                
    # def productos_vendidos(self):
    #     productos_vendidos = FacturaProducto.objects.none()

    #     if self.producto_id:
    #         producto_seleccionado = Producto.objects.get(id=self.producto_id)
    #         productos_vendidos = FacturaProducto.objects.filter(producto=producto_seleccionado)
    #     elif self.categoria:
    #         productos_categoria = Producto.objects.filter(categoria__nombre=self.categoria)
    #         productos_vendidos = FacturaProducto.objects.filter(producto__in=productos_categoria)

    #     if productos_vendidos.exists():
    #         ultima_factura = productos_vendidos.order_by('-factura__fecha').first()
    #         ultimo_lunes = ultima_factura.factura.fecha if ultima_factura else timezone.now()
    #         ultimo_dia = ultimo_lunes.weekday()          
    #         if ultimo_dia != 0:
    #             ultimo_lunes = ultimo_lunes - timedelta(days=ultimo_dia)
                
    #         primera_factura = productos_vendidos.order_by('factura__fecha').first()
    #         primer_lunes = primera_factura.factura.fecha if primera_factura else ultimo_lunes - timedelta(days=92)
    #         primer_dia = primer_lunes.weekday()
    #         if primer_dia != 0:
    #             primer_lunes = primer_lunes + timedelta(days=7-primer_dia)
                
    #         dif_fecha = (ultimo_lunes - primer_lunes).days            
    #         if dif_fecha > 92:
    #             primer_lunes = ultimo_lunes - timedelta(days=92)
    #             primer_dia = primer_lunes.weekday()
    #             if primer_dia != 0:
    #                 primer_lunes = primer_lunes + timedelta(days=7-primer_dia)


    #         if self.dia_semana or self.media_semana:
    #             productos_vendidos = productos_vendidos.filter(factura__fecha__range=(primer_lunes, ultimo_lunes))

    #         if self.fecha_inicio and self.fecha_fin:                
    #             productos_vendidos = productos_vendidos.filter(factura__fecha__range=[self.fecha_inicio, self.fecha_fin])
                
    #         if self.mes and self.ano:
    #             ano = int(self.ano)
    #             if self.mes != "0":
    #                 mes = int(self.mes)
    #                 productos_vendidos = productos_vendidos.filter(factura__fecha__month=mes, factura__fecha__year=ano)
    #             else:
    #                 productos_vendidos = productos_vendidos.filter(factura__fecha__year=ano)

    #     return productos_vendidos
    
    # def calcular_cantidad_vendida(self, productos_vendidos):
    #     if self.dia_semana:
    #         productos_vendidos = productos_vendidos.filter(factura__fecha__week_day=int(self.dia_semana))
        
    #     if self.media_semana:
    #         if self.media_semana == "m_j":
    #             productos_vendidos = productos_vendidos.filter(factura__fecha__week_day__in=[3, 4, 5])
    #         else:
    #             productos_vendidos = productos_vendidos.filter(factura__fecha__week_day__in=[6, 7, 1])
        
    #     self.cantidad_vendida = productos_vendidos.aggregate(total_vendido=Sum('cantidad'))['total_vendido'] or 0  
        
               
    # def calcular_cantidad_dias(self, productos_vendidos):
    #     if self.fecha_inicio and self.fecha_fin:
    #         self.cantidad_dias = (self.fecha_fin - self.fecha_inicio).days         
    #     elif self.dia_semana:
    #         try:
    #             if productos_vendidos.exists():
    #                 primera_fecha = productos_vendidos.earliest('factura__fecha').factura.fecha
    #                 ultima_fecha = productos_vendidos.latest('factura__fecha').factura.fecha
    #                 dia_semana_deseado = int(self.dia_semana) - 2
    #                 cantidad_dias_semana = 0
    #                 fecha_actual = primera_fecha
                    
    #                 while fecha_actual <= ultima_fecha:
    #                     if fecha_actual.weekday() == dia_semana_deseado:  
    #                         cantidad_dias_semana += 1
    #                     fecha_actual += timedelta(days=1)  
                        
    #                 self.cantidad_dias = cantidad_dias_semana                    
    #             else:
    #                 self.cantidad_dias = 0
    #         except Producto.DoesNotExist:
    #             print(f"Producto {self.producto_nombre} no existe.")
    #         except ProductoCategoria.DoesNotExist:
    #             print(f"Categoría {self.categoria} no existe.")
    #     elif self.media_semana:
    #         try:
    #             if productos_vendidos.exists():
    #                 primera_fecha = productos_vendidos.earliest('factura__fecha').factura.fecha
    #                 ultima_fecha = productos_vendidos.latest('factura__fecha').factura.fecha
    #                 cantidad_dias_semana = 0
    #                 fecha_actual = primera_fecha
                    
    #                 if self.media_semana == "m_j":
    #                     while fecha_actual <= ultima_fecha:
    #                         if fecha_actual.weekday() in [1, 2, 3]: 
    #                             cantidad_dias_semana += 1
    #                         fecha_actual += timedelta(days=1)
                            
    #                     self.cantidad_dias = cantidad_dias_semana / 2
    #                 else:
    #                     while fecha_actual <= ultima_fecha:
    #                         if fecha_actual.weekday() in [4, 5, 6]:  
    #                             cantidad_dias_semana += 1
    #                         fecha_actual += timedelta(days=1)
                            
    #                     self.cantidad_dias = cantidad_dias_semana / 2
    #             else:
    #                 self.cantidad_dias = 0
    #         except Producto.DoesNotExist:
    #             print(f"Producto {self.producto_nombre} no existe.")
    #         except ProductoCategoria.DoesNotExist:
    #             print(f"Categoría {self.categoria} no existe.")
    #     elif self.mes and self.ano:
    #         if self.mes != "0":
    #             mes = int(self.mes)
    #             ano = int(self.ano)
    #             _, self.cantidad_dias = calendar.monthrange(ano, mes)
    #         else:
    #             ano = int(self.ano)
    #             if calendar.isleap(ano):
    #                 self.cantidad_dias = 366
    #             else:
    #                 self.cantidad_dias = 365
                
    #     else:
    #         self.cantidad_dias = 0

                   


    # def calcular_dia_venta(self, productos_vendidos):
    #     if self.fecha_inicio and self.fecha_fin:
    #         fechas = [producto.factura.fecha for producto in productos_vendidos]
            
    #         if not fechas:
    #             self.dia_venta = 0
    #             self.dia_no_venta = 0
    #             return
            
    #         dias_con_ventas = set(fechas)
                      
    #         self.dia_venta = len(dias_con_ventas)
    #         self.dia_no_venta = self.cantidad_dias - self.dia_venta
            
    #     elif self.dia_semana: 
    #         fechas_ventas = [producto.factura.fecha for producto in productos_vendidos]
            
    #         dias_con_ventas = set(
    #             fecha for fecha in fechas_ventas if fecha.weekday() == int(self.dia_semana) - 2
    #         )

    #         self.dia_venta = len(dias_con_ventas)
    #         self.dia_no_venta = self.cantidad_dias - self.dia_venta
            
            
            
            
            
            
            
            
            
            
            
            
            # dias_con_ventas = set()  
            # fechas_ventas = [producto.factura.fecha for producto in productos_vendidos]


            # self.dia_venta = len(dias_con_ventas)
            # self.dia_no_venta = self.cantidad_dias - self.dia_venta

    

    def calcular_dia_no_venta():
        pass

    def calcular_promedio():
        pass

    def calcular_no_vendidos():
        pass