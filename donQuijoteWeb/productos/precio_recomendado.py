from .models import Producto, Insumos, ProductoInsumos


def precio_recomendado():
    precio_recomendado= 0
    
    insumos = Insumos.objects.all()
    prod_insumos = ProductoInsumos.objects.filter(producto__nombre__in=Producto.objects.values_list("nombre", flat=True))
    
    for prod_insumo in prod_insumos:
        for insumo in insumos:
            if str(insumo.nombre) == str(prod_insumo.insumo) and insumo.unidad == "Kg" and prod_insumo.unidad == "Gr":
                precio_recomendado+= (insumo.precio/1000) * prod_insumo.cantidad

    print(f"PRECIO RECOMENDADO: {precio_recomendado}")
        