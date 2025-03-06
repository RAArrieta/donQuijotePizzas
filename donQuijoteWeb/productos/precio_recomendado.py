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

    epec = ultimo_gasto("EPEC")
    agua = ultimo_gasto("Aguas Cordobesas")
    gas = ultimo_gasto("Gas")
    telefono = ultimo_gasto("Telefonía")
    internet = ultimo_gasto("Internet")
    servicios = ultimo_gasto("Otros Servicios")
    inmueble = ultimo_gasto("Inmueble")
    municipalidad = ultimo_gasto("Municipalidad")

    # Filtrar los sueldos en los últimos 30 días
    rango_30_dias = timezone.now().date() - timedelta(days=30)
    sueldos = Gastos.objects.filter(proveedor__nombre="Sueldos", fecha__gte=rango_30_dias).order_by("-fecha")

    sueldos_30d = sum(sueldo.monto for sueldo in sueldos) if sueldos.exists() else 0

    # Mostrar los gastos individuales
    print(f"Último gasto en EPEC: {epec}")
    print(f"Último gasto en Agua: {agua}")
    print(f"Último gasto en Gas: {gas}")
    print(f"Último gasto en Teléfono: {telefono}")
    print(f"Último gasto en Internet: {internet}")
    print(f"Último gasto en Servicios: {servicios}")
    print(f"Último gasto en Alquiler: {inmueble}")
    print(f"Último gasto en Municipalidad: {municipalidad}")

    # Calcular el gasto total
    gasto_total = epec + agua + gas + telefono + internet + servicios + inmueble + municipalidad + sueldos_30d

    print(f"Gasto Total: {gasto_total}")                                

    #CALCULO LA CANTIDAD DE PRODUCTOS POR MES
    fecha_inicio = now().date() - timedelta(days=30)

    ventas_por_categoria = (
        FacturaProducto.objects
        .filter(factura__fecha__gte=fecha_inicio)
        .values("producto__categoria__nombre")  
        .annotate(total_vendido=Sum("cantidad"))
        .order_by("-total_vendido")  
    )
    pizzas_vendidas = next(
        (item["total_vendido"] for item in ventas_por_categoria if item["producto__categoria__nombre"] == "Pizzas"),
        0
    )

    print(f"Cantidad de pizzas vendidas en los últimos 30 días: {pizzas_vendidas}")

    empanadas_vendidas = next(
        (item["total_vendido"] for item in ventas_por_categoria if item["producto__categoria__nombre"] == "Empanadas"),
        0
    )/12

    print(f"Cantidad de Empanadas vendidas en los últimos 30 días: {empanadas_vendidas}")

    sandwichs_vendidos = next(
        (item["total_vendido"] for item in ventas_por_categoria if item["producto__categoria__nombre"] == "Sandwichs"),
        0
    )

    print(f"Cantidad de Sandwichs vendidas en los últimos 30 días: {sandwichs_vendidos}")

    minutas_vendidas = next(
        (item["total_vendido"] for item in ventas_por_categoria if item["producto__categoria__nombre"] == "Minutas"),
        0
    )

    print(f"Cantidad de Minutas vendidas en los últimos 30 días: {minutas_vendidas}")

    cant_prod = pizzas_vendidas + empanadas_vendidas + sandwichs_vendidos + minutas_vendidas

    print(f"Cantidad de Productos Vendidos: {cant_prod}")

    #CALCULO EL COSTO DE CADA PRODUCTO
    insumos = Insumos.objects.all()
    prod_insumos = ProductoInsumos.objects.all()

    prod_precios_rec = {}

    for prod_insumo in prod_insumos:
        precio_recomendado = 0  
        precio_recomendado_final = 0  
        # print(prod_insumo.producto)

        for insumo in insumos:
            if str(insumo.nombre) == str(prod_insumo.insumo):
                print(f"{insumo.nombre}: {prod_insumo.cantidad} {prod_insumo.unidad} x {insumo.precio}")
                if insumo.unidad == "Kg" and prod_insumo.unidad == "Gr":
                    precio_recomendado += (insumo.precio / 1000) * prod_insumo.cantidad
                else:
                    precio_recomendado += insumo.precio * prod_insumo.cantidad

        producto_nombre = str(prod_insumo.producto)
        prod_precios_rec[producto_nombre] = prod_precios_rec.get(producto_nombre, 0) + precio_recomendado

    prod_actualizo = Producto.objects.all()
    
    for clave, valor in prod_precios_rec.items():
        # print(type(clave))
        # print(f"{clave}: {valor}")
        for act in prod_actualizo:
            if clave == str(act):
                print(f"prod_precios_rec: {clave}, Producto que actualizo: {act}, Costo Producto: {valor} ")
                print(f"Costo: {valor}, GastosT: {gasto_total}, Prod_Vendidos: {cant_prod}")
                precio_recomendado_final = ( valor * 2.1 ) + ( gasto_total / cant_prod )
                print(f"Precio Recomendado para {act}:{precio_recomendado_final}")


                Producto.objects.filter(nombre=act).update(precio_rec=precio_recomendado_final)

