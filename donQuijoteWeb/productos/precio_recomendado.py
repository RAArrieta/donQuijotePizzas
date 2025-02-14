from .models import Producto, Insumos, ProductoInsumos


def precio_recomendado():
    precio_recomendado= 0
    
    insumos = Insumos.objects.all()
    prod_insumos = ProductoInsumos.objects.filter(producto__nombre__in=Producto.objects.values_list("nombre", flat=True))
    
    prod_precios_rec={}
    
    for prod_insumo in prod_insumos:
        for insumo in insumos:
            if str(insumo.nombre) == str(prod_insumo.insumo) and insumo.unidad == "Kg" and prod_insumo.unidad == "Gr":
                precio_recomendado+= (insumo.precio/1000) * prod_insumo.cantidad
            if str(insumo.nombre) == str(prod_insumo.insumo) and insumo.unidad == "Unid" and prod_insumo.unidad == "Unid":
                precio_recomendado+= insumo.precio * prod_insumo.cantidad
        print(f"PRECIO RECOMENDADO {prod_insumo.producto}: {precio_recomendado}")
        
        
        
        
def precio_recomendado():
    insumos = Insumos.objects.all()
    prod_insumos = ProductoInsumos.objects.all()

    prod_precios_rec = {}

    for prod_insumo in prod_insumos:
        precio_recomendado = 0  

        for insumo in insumos:
            if str(insumo.nombre) == str(prod_insumo.insumo):
                if insumo.unidad == "Kg" and prod_insumo.unidad == "Gr":
                    precio_recomendado += (insumo.precio / 1000) * prod_insumo.cantidad
                elif insumo.unidad == "Unid" and prod_insumo.unidad == "Unid":
                    precio_recomendado += insumo.precio * prod_insumo.cantidad

        producto_nombre = str(prod_insumo.producto)
        prod_precios_rec[producto_nombre] = prod_precios_rec.get(producto_nombre, 0) + precio_recomendado

    for clave, valor in prod_precios_rec.items():
        print(f"{clave}: {valor}")
        