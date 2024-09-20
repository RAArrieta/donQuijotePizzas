from datetime import timedelta
from facturas.models import FacturaProducto
from productos.models import Producto, ProductoCategoria
from django.db.models import Sum, Min, Max, Avg, Count

class Estadisticas:
    def __init__(self, producto_id,  producto_nombre, categoria, cantidad_vendida, fecha_inicio, fecha_fin, dia_semana, cantidad_dias):
        self.producto_id = producto_id
        self.producto_nombre = producto_nombre
        self.categoria= categoria
        self.cantidad_vendida = cantidad_vendida
        # self.cantidad_promedio = cantidad_promedio
        # self.cantidad_minima = cantidad_minima
        # self.cantidad_maxima = cantidad_maxima
        # self.cantidad_no_vendida = cantidad_no_vendida
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.dia_semana = dia_semana
        self.cantidad_dias = cantidad_dias
        
    def calcular_cantidad_vendida(self):
        if self.producto_id:
            try:
                producto_seleccionado = Producto.objects.get(id=self.producto_id)
                productos_vendidos = FacturaProducto.objects.filter(
                    producto=producto_seleccionado
                )
                if self.fecha_inicio and self.fecha_fin:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__range=[self.fecha_inicio, self.fecha_fin]
                    )
                if self.dia_semana:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__week_day=int(self.dia_semana)
                    )
                self.cantidad_vendida = productos_vendidos.aggregate(total_vendido=Sum('cantidad'))['total_vendido'] or 0  
            except Producto.DoesNotExist:
                print(f"Producto {self.producto_nombre} no existe.")
                
        elif self.categoria:
            try:
                productos_categoria = Producto.objects.filter(categoria__nombre=self.categoria)
                productos_vendidos = FacturaProducto.objects.filter(
                    producto__in=productos_categoria
                )
                if self.fecha_inicio and self.fecha_fin:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__range=[self.fecha_inicio, self.fecha_fin]
                    )
                if self.dia_semana:
                    productos_vendidos = productos_vendidos.filter(
                        factura__fecha__week_day=int(self.dia_semana)
                    )
                self.cantidad_vendida = productos_vendidos.aggregate(total_vendido=Sum('cantidad'))['total_vendido'] or 0
            except ProductoCategoria.DoesNotExist:
                print(f"Categoría {self.categoria} no existe.")
                
                
    def calcular_cantidad_dias(self):
        if self.fecha_inicio and self.fecha_fin:
            self.cantidad_dias = (self.fecha_fin - self.fecha_inicio).days + 1
        elif self.dia_semana:
            try:
                if self.producto_id:
                    producto_seleccionado = Producto.objects.get(id=self.producto_id)
                    productos_vendidos = FacturaProducto.objects.filter(
                        producto=producto_seleccionado,
                        factura__fecha__week_day=int(self.dia_semana)
                    )
                elif self.categoria:
                    productos_categoria = Producto.objects.filter(categoria__nombre=self.categoria)
                    productos_vendidos = FacturaProducto.objects.filter(
                        producto__in=productos_categoria,
                        factura__fecha__week_day=int(self.dia_semana)
                    )
                else:
                    productos_vendidos = FacturaProducto.objects.none()

                if productos_vendidos.exists():
                    # Obtener la fecha más antigua y más reciente de ventas
                    primera_fecha = productos_vendidos.earliest('factura__fecha').factura.fecha
                    ultima_fecha = productos_vendidos.latest('factura__fecha').factura.fecha

                    dia_semana_deseado = int(self.dia_semana)
                    cantidad_dias_semana = 1

                    fecha_actual = primera_fecha
                    while fecha_actual <= ultima_fecha:
                        if fecha_actual.weekday() == dia_semana_deseado:  
                            cantidad_dias_semana += 1
                        fecha_actual += timedelta(days=1)  
                        
                    self.cantidad_dias = cantidad_dias_semana

                # if productos_vendidos.exists():
                #     # Obtener la fecha más antigua y más reciente de ventas
                #     primera_fecha = productos_vendidos.earliest('factura__fecha').factura.fecha
                #     ultima_fecha = productos_vendidos.latest('factura__fecha').factura.fecha
                #     print(f"Primera fecha: {primera_fecha}, Ultima fecha: {ultima_fecha}")
                    
                else:
                    self.cantidad_dias = 0
            except Producto.DoesNotExist:
                print(f"Producto {self.producto_nombre} no existe.")
            except ProductoCategoria.DoesNotExist:
                print(f"Categoría {self.categoria} no existe.")
        else:
            self.cantidad_dias = 0

                
    # def calcular_cantidad_dias(self):
    #     if self.fecha_inicio and self.fecha_fin:
    #         self.cantidad_dias = (self.fecha_fin - self.fecha_inicio).days + 1
    #     elif self.dia_semana:
    #         self.cantidad_dias = 24
            
    #         productos_vendidos = productos_vendidos.filter(factura__fecha__week_day=int(self.dia_semana))
    #         print(productos_vendidos)
    #         # Obtener la fecha más antigua y más reciente de ventas los días miércoles.
    #         primera_fecha = productos_vendidos.earliest('factura__fecha').factura.fecha
    #         ultima_fecha = productos_vendidos.latest('factura__fecha').factura.fecha
    #         print(f"Primera fecha: {primera_fecha}, Ultima fecha: {ultima_fecha}")


    #     else:
    #         self.cantidad_dias = 0
                    
    def calcular_minimo():
        pass

    def calcular_maximo():
        pass

    def calcular_promedio():
        pass

    def calcular_no_vendidos():
        pass