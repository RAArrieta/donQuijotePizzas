from .models import Producto, Insumos, ProductoInsumos
from facturas.models import FacturaProducto
from gastos.models import Gastos
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum


def precio_recomendado():
    def ultimo_gasto(proveedor):
        gasto = Gastos.objects.filter(proveedor__nombre=proveedor).order_by("-fecha").first()
        return gasto.monto if gasto else 0

    #OBTENGO EL ULTIMO GASTO DE SERVIVIOS
    epec = ultimo_gasto("EPEC")
    agua = ultimo_gasto("Aguas Cordobesas")
    gas = ultimo_gasto("Gas")
    telefono = ultimo_gasto("Telefonía")
    internet = ultimo_gasto("Internet")
    servicios = ultimo_gasto("Otros Servicios")
    inmueble = ultimo_gasto("Inmueble")
    municipalidad = ultimo_gasto("Municipalidad")
    
    #CALCULO GASTO DE COMBUSTIBLE Y DE SUELDO DEL MES
    rango_30_dias = timezone.now().date() - timedelta(days=30)
    sueldos = Gastos.objects.filter(proveedor__nombre="Sueldos", fecha__gte=rango_30_dias).order_by("-fecha")
    combustible = Gastos.objects.filter(proveedor__nombre="Combustible", fecha__gte=rango_30_dias).order_by("-fecha")
    sueldos_30d = sum(sueldo.monto for sueldo in sueldos) if sueldos.exists() else 0
    combustible_30d = sum(comb.monto for comb in combustible) if combustible.exists() else 0

    #CALCULO EL GASTO TOTAL MENSUAL
    gasto_total = epec + agua + gas + telefono + internet + servicios + inmueble + municipalidad + sueldos_30d + combustible_30d

    #CALCULO LA CANTIDAD DE PRODUCTOS POR MES
    fecha_inicio = now().date() - timedelta(days=30)

    ventas_por_categoria = (
        FacturaProducto.objects
        .filter(factura__fecha__gte=fecha_inicio)
        .values("producto__categoria__nombre")  
        .annotate(total_vendido=Sum("cantidad"))
        .order_by("-total_vendido")  
    )
    pizzas_vendidas = next((item["total_vendido"] for item in ventas_por_categoria if item["producto__categoria__nombre"] == "Pizzas"), 0)
    empanadas_vendidas = next((item["total_vendido"] for item in ventas_por_categoria if item["producto__categoria__nombre"] == "Empanadas"), 0)/12
    sandwichs_vendidos = next((item["total_vendido"] for item in ventas_por_categoria if item["producto__categoria__nombre"] == "Sandwichs"), 0)
    minutas_vendidas = next((item["total_vendido"] for item in ventas_por_categoria if item["producto__categoria__nombre"] == "Minutas"), 0)

    cant_prod = pizzas_vendidas + empanadas_vendidas + sandwichs_vendidos + minutas_vendidas

    #CALCULO EL COSTO DE CADA PRODUCTO
    insumos = Insumos.objects.all()
    prod_insumos = ProductoInsumos.objects.all()

    prod_precios_rec = {}

    for prod_insumo in prod_insumos:
        precio_recomendado = 0  
        precio_recomendado_final = 0  
        for insumo in insumos:
            if str(insumo.nombre) == str(prod_insumo.insumo):
                if insumo.unidad == "Kg" and prod_insumo.unidad == "Gr":
                    precio_recomendado += (insumo.precio / 1000) * prod_insumo.cantidad
                else:
                    precio_recomendado += insumo.precio * prod_insumo.cantidad

        producto_nombre = str(prod_insumo.producto)
        prod_precios_rec[producto_nombre] = prod_precios_rec.get(producto_nombre, 0) + precio_recomendado

    prod_actualizo = Producto.objects.all()
    
    for clave, valor in prod_precios_rec.items():
        for act in prod_actualizo:
            if clave == str(act):              
                if cant_prod == 0:
                    precio_recomendado_final = 1
                else:
                    precio_recomendado_final = ( valor * 2.1 ) + ( gasto_total / cant_prod )
                    
                Producto.objects.filter(nombre=act).update(precio_rec=precio_recomendado_final)

