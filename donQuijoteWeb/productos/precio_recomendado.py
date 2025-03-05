from .models import Producto, Insumos, ProductoInsumos
from facturas.models import FacturaProducto
from gastos.models import Gastos
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum


def precio_recomendado():
    #CALCULO LA SUMA DE LOS GASTOS
    epec = Gastos.objects.filter(proveedor__nombre="EPEC").order_by("-fecha").first()
    agua = Gastos.objects.filter(proveedor__nombre="Aguas Cordobesas").order_by("-fecha").first()
    gas = Gastos.objects.filter(proveedor__nombre="Gas").order_by("-fecha").first()
    telefono = Gastos.objects.filter(proveedor__nombre="Telefonía").order_by("-fecha").first()
    internet = Gastos.objects.filter(proveedor__nombre="Internet").order_by("-fecha").first()
    servicios = Gastos.objects.filter(proveedor__nombre="Otros Servicios").order_by("-fecha").first()

    inmueble = Gastos.objects.filter(proveedor__nombre="Inmueble").order_by("-fecha").first()

    municipalidad = Gastos.objects.filter(proveedor__nombre="Municipalidad").order_by("-fecha").first()

    rango_30_dias = timezone.now().date() - timedelta(days=30)
    # sueldos = Gastos.objects.filter(proveedor__nombre="Sueldos").order_by("-fecha").first()
    sueldos = Gastos.objects.filter(proveedor__nombre="Sueldos", fecha__gte=rango_30_dias).order_by("-fecha")
    
    sueldos_30d = 0
    gasto_total = 0

    if sueldos.exists():
        print("SUELDOS")
        for sueldo in sueldos:
            sueldos_30d += sueldo.monto
            print(f"Fecha: {sueldo.fecha}, Monto: {sueldo.monto}")
    else:
        print("No hay registros de sueldos en los últimos 30 días.")

    print(f"Monto Sueldo Total: {sueldos_30d}")

    if epec or agua or gas or telefono or internet or servicios or inmueble or municipalidad:  
        print(f"Último gasto en EPEC: {epec.monto}")
        print(f"Último gasto en Agua: {agua.monto}")
        print(f"Último gasto en gas: {gas.monto}")
        print(f"Último gasto en telefono: {telefono.monto}")
        print(f"Último gasto en internet: {internet.monto}")
        print(f"Último gasto en servicios: {servicios.monto}")
        print(f"Último gasto en alquiler: {inmueble.monto}")
        print(f"Último gasto en municipalidad: {municipalidad.monto}")

        gasto_total = epec.monto + agua.monto + gas.monto + telefono.monto + internet.monto + servicios.monto + inmueble.monto + municipalidad.monto + sueldos_30d

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

