from .models import Producto, Insumos, ProductoInsumos
        
def precio_recomendado():
    insumos = Insumos.objects.all()
    prod_insumos = ProductoInsumos.objects.all()

    prod_precios_rec = {}

    for prod_insumo in prod_insumos:
        precio_recomendado = 0  
        print(prod_insumo.producto)

        for insumo in insumos:
            if str(insumo.nombre) == str(prod_insumo.insumo):
                print(f"{insumo.nombre}: {prod_insumo.cantidad} {prod_insumo.unidad} x {insumo.precio}")
                if insumo.unidad == "Kg" and prod_insumo.unidad == "Gr":
                    precio_recomendado += (insumo.precio / 1000) * prod_insumo.cantidad
                else:
                    precio_recomendado += insumo.precio * prod_insumo.cantidad

        producto_nombre = str(prod_insumo.producto)
        prod_precios_rec[producto_nombre] = prod_precios_rec.get(producto_nombre, 0) + precio_recomendado

    for clave, valor in prod_precios_rec.items():
        print(f"{clave}: {valor}")
        