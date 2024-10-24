import calendar
from datetime import timedelta
from django.utils import timezone
from facturas.models import FacturaProducto, Facturas
from productos.models import Producto
from django.db.models import Sum, Count

class Estadisticas:
    env = False
    def __init__(self, producto_id,  producto_nombre, categoria, cantidad_vendida, cantidad_promedio, cantidad_minima, cantidad_maxima, dia_venta, dia_no_venta, fecha_inicio, fecha_fin, dia_semana, media_semana, mes, ano, cantidad_dias):
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.categoria= categoria
        
        self.cantidad_vendida = cantidad_vendida
        self.cantidad_promedio = cantidad_promedio
        self.cantidad_minima = cantidad_minima
        self.cantidad_maxima = cantidad_maxima
        
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.dia_semana = dia_semana
        self.media_semana = media_semana
        self.mes = mes
        self.ano = ano
        self.cantidad_dias = cantidad_dias
        
        self.dia_venta = dia_venta
        self.dia_no_venta = dia_no_venta
        
    def estadisticas(self):
            try:
                rango_facturado = Estadisticas.rango_facturado(self)
                Estadisticas.calculo_cantidad_dias(self, rango_facturado)
                productos_vendidos = Estadisticas.productos_vendidos(self, rango_facturado)
                Estadisticas.calculo_cantidad_vendida(self, productos_vendidos)
                Estadisticas.calculo_cantidad_promedio(self)
                Estadisticas.calculo_dia_venta(self, productos_vendidos)
 
            except Producto.DoesNotExist:
                print(f"Producto {self.producto_nombre} no existe.")
                
    def rango_facturado(self):
        #Traigo todas las facturas
        total_facturas = FacturaProducto.objects.all()
        
        if total_facturas.exists():
            #Consigo la ultima fecha de facturacion y la convierto en el ultimo lunes
            ultima_factura = total_facturas.order_by('-factura__fecha').first()
            ultima_fecha = ultima_factura.factura.fecha if ultima_factura else timezone.now().date()
            ultima_fecha_for = ultima_fecha.weekday()   
            if ultima_fecha_for != 0:
                ultima_fecha = ultima_fecha - timedelta(days=ultima_fecha_for)
               
            #Consigo la primer fecha de facturacion y la convierto en el primer lunes 
            primera_factura = total_facturas.order_by('factura__fecha').first()
            primer_fecha = primera_factura.factura.fecha if primera_factura else ultima_fecha - timedelta(days=92)
            primer_fecha_for = primer_fecha.weekday()
            if primer_fecha_for != 0:
                primer_fecha = primer_fecha + timedelta(days=7-primer_fecha_for)
                
            dif_fecha = (ultima_fecha - primer_fecha).days
                                
            #Pongo un limite de 93 días a las rango para estadisticas
            if dif_fecha > 93:
                primer_fecha = ultima_fecha - timedelta(days=93)
                primer_fecha_for = primer_fecha.weekday()
                if primer_fecha_for != 0:
                    primer_fecha = primer_fecha + timedelta(days=7-primer_fecha_for) 
                    dif_fecha = (ultima_fecha - primer_fecha).days   
                
            #Alineo las fechas ingresadas por el usuario, por si se exede en las fechas de busqueda
            if self.fecha_inicio and self.fecha_fin:
                if self.fecha_inicio < primera_factura.factura.fecha or self.fecha_inicio > self.fecha_fin or self.fecha_inicio > timezone.now().date():
                    self.fecha_inicio = primera_factura.factura.fecha if primera_factura else ultima_fecha - timedelta(days=93)
                    
                if self.fecha_fin > timezone.now().date() or self.fecha_fin > ultima_factura.factura.fecha:
                    self.fecha_fin = timezone.now().date()

            return {'primer_fecha': primer_fecha, 'ultima_fecha': ultima_fecha}
        else:
            return {'primer_fecha': timezone.now().date() - timedelta(days=93), 'ultima_fecha': timezone.now().date()}
    
    def calculo_cantidad_dias(self, rango_facturado):
        primer_fecha = rango_facturado["primer_fecha"]
        ultima_fecha = rango_facturado["ultima_fecha"]
        cantidad_lunes = 0

        if self.fecha_inicio and self.fecha_fin:
            
            primer_fecha = self.fecha_inicio
            ultima_fecha = self.fecha_fin
            fecha_actual = primer_fecha
            while fecha_actual <= ultima_fecha:
                if fecha_actual.weekday() == 0: 
                    cantidad_lunes += 1
                fecha_actual += timedelta(days=1)
        elif self.dia_semana or self.media_semana:    
            cantidad_lunes = (ultima_fecha - primer_fecha).days / 7 + 1
        elif self.mes and self.ano:
            ano = int(self.ano)
            if self.mes != "0":
                mes = int(self.mes)
                _, dias_mes = calendar.monthrange(ano, mes)
                for dia in range(1, dias_mes + 1):
                    if calendar.weekday(ano, mes, dia) == 0:  
                        cantidad_lunes += 1
            else:
                cantidad_lunes = 0  
                for mes in range(1, 13):  
                    _, dias_mes = calendar.monthrange(ano, mes)
                    for dia in range(1, dias_mes + 1):
                        if calendar.weekday(ano, mes, dia) == 0:  
                            cantidad_lunes += 1
                   
        if self.fecha_inicio and self.fecha_fin:
            self.cantidad_dias = (self.fecha_fin - self.fecha_inicio).days + 1 - cantidad_lunes
        
        if self.dia_semana or self.media_semana:
            self.cantidad_dias = (ultima_fecha - primer_fecha).days / 7
                              
        if self.mes and self.ano:
            ano = int(self.ano)
            if self.mes != "0":
                mes = int(self.mes)
                _, dias_mes = calendar.monthrange(ano, mes)
                self.cantidad_dias = dias_mes - cantidad_lunes
            else:
                if calendar.isleap(ano):
                    self.cantidad_dias = 366 - cantidad_lunes
                else:
                    self.cantidad_dias = 365 - cantidad_lunes
            
        self.cantidad_dias = int(self.cantidad_dias)    
        
    def productos_vendidos(self, rango_facturado):
        productos_vendidos = FacturaProducto.objects.none()
        primer_fecha = rango_facturado["primer_fecha"]
        ultima_fecha = rango_facturado["ultima_fecha"]

        if self.producto_id:
            producto_seleccionado = Producto.objects.get(id=self.producto_id) #aqui creo producto_seleccionado solo con el producto
            productos_vendidos = FacturaProducto.objects.filter(producto=producto_seleccionado)
        elif self.categoria:
            productos_categoria = Producto.objects.filter(categoria__nombre=self.categoria)#aqui creo producto_categoria solo con la categoria seleccionada
            productos_vendidos = FacturaProducto.objects.filter(producto__in=productos_categoria)           
        else:
            self.env = True
            facturas_con_envio = Facturas.objects.filter(envio__gt=0)   #aqui solo quiero traer las facturas con envios sin productos ni categoria para luego poder contabilizar
            productos_vendidos = FacturaProducto.objects.filter(factura__in=facturas_con_envio)

        if productos_vendidos.exists():
            if self.fecha_inicio and self.fecha_fin:                
                productos_vendidos = productos_vendidos.filter(factura__fecha__range=[self.fecha_inicio, self.fecha_fin])

            if self.dia_semana or self.media_semana:
                productos_vendidos = productos_vendidos.filter(factura__fecha__range=(primer_fecha, ultima_fecha))
  
            if self.mes and self.ano:
                ano = int(self.ano)
                if self.mes != "0":
                    mes = int(self.mes)
                    productos_vendidos = productos_vendidos.filter(factura__fecha__month=mes, factura__fecha__year=ano)
                else:
                    productos_vendidos = productos_vendidos.filter(factura__fecha__year=ano)
        return productos_vendidos
    
    def calculo_cantidad_vendida(self, productos_vendidos):
        if self.dia_semana:            
            productos_vendidos = productos_vendidos.filter(factura__fecha__week_day=int(self.dia_semana))
        
        if self.media_semana:            
            if self.media_semana == "m_j":
                productos_vendidos = productos_vendidos.filter(factura__fecha__week_day__in=[3, 4, 5])
            else:
                productos_vendidos = productos_vendidos.filter(factura__fecha__week_day__in=[6, 7, 1])          
                                
            productos_vendidos_por_semana = productos_vendidos.values('factura__fecha__week')\
                .annotate(total_vendido=Sum('cantidad'))\
                .filter(total_vendido__gt=0)\
                .order_by('total_vendido')
                
            self.cantidad_minima = productos_vendidos_por_semana.first()['total_vendido'] if productos_vendidos_por_semana.exists() else 0
            self.cantidad_maxima = productos_vendidos_por_semana.last()['total_vendido'] if productos_vendidos_por_semana.exists() else 0

        else:
            productos_vendidos_por_dia = (productos_vendidos
                    .values('factura__fecha')
                    .annotate(total_vendido=Sum('cantidad'))
                    .filter(total_vendido__gt=0) 
                    .order_by('total_vendido')
                )               

            cantidad_minima = productos_vendidos_por_dia.first()
            self.cantidad_minima = cantidad_minima['total_vendido']
            cantidad_maxima = productos_vendidos_por_dia.last()
            self.cantidad_maxima = cantidad_maxima['total_vendido']
        
        self.cantidad_vendida = productos_vendidos.aggregate(total_vendido=Sum('cantidad'))['total_vendido'] or 0 
            
        if self.env == True:
            self.cantidad_vendida = productos_vendidos.values('factura').distinct().count()

            if self.media_semana:
                envios_por_dia = productos_vendidos.values('factura__fecha__week')\
                    .annotate(cantidad_facturas=Count('factura', distinct=True))\
                    .filter(cantidad_facturas__gt=0)\
                    .order_by('cantidad_facturas')
                self.cantidad_minima = envios_por_dia.first()['cantidad_facturas'] if envios_por_dia.exists() else 0
                self.cantidad_maxima = envios_por_dia.last()['cantidad_facturas'] if envios_por_dia.exists() else 0
            else:
                envios_por_dia = productos_vendidos.filter(factura__envio__gt=0) \
                    .values('factura__fecha') \
                    .annotate(cantidad_facturas=Count('factura', distinct=True)) \
                    .order_by('cantidad_facturas')
            
                self.cantidad_minima = envios_por_dia.first().get('cantidad_facturas', 0)
                self.cantidad_maxima = envios_por_dia.last().get('cantidad_facturas', 0)

            self.env == False            
        
    def calculo_cantidad_promedio(self):           
        if self.cantidad_dias > 0 and self.cantidad_vendida > 0:
            self.cantidad_promedio = round(self.cantidad_vendida / self.cantidad_dias, 1)
        else:
            self.cantidad_promedio = 0                  

    def calculo_dia_venta(self, productos_vendidos):
        rango_fechas = set(producto.factura.fecha for producto in productos_vendidos)
        
        if (self.fecha_inicio and self.fecha_fin) or self.mes or self.ano:
            self.dia_venta = len(list(rango_fechas))
            self.dia_no_venta = self.cantidad_dias - self.dia_venta
            
        if self.dia_semana:
            dias_coincidentes = [fecha for fecha in rango_fechas if fecha.weekday() == int(self.dia_semana) - 2]

            self.dia_venta = len(dias_coincidentes)
            self.dia_no_venta = int(self.cantidad_dias - self.dia_venta)

