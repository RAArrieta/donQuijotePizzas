from productos.models import Producto
from .carro import Carro

def chequear_stock(request, producto):
    productos_stock = Producto.objects.all()
    valor = True
    cant_total = total_prod_pedido(request, producto, valor)

    for p_s in productos_stock:
        # print(p_s)
        # print(f"Stock Prod: {p_s.stock}, Stock Cat: {p_s.categoria.stock}")
        # print(f"Cantid Prod: {p_s.cantidad} > 0")
        # print(f"Cantid Cat: {p_s.categoria.cantidad} > 0")
        # print(f"Cantid Cat: {p_s.categoria.cantidad} + cant_total {cant_total} : {p_s.categoria.cantidad - cant_total} > 1.0")
        if p_s.id == producto.id:
            if p_s.stock and p_s.categoria.stock and p_s.cantidad > 0 and p_s.categoria.cantidad > 0 and (p_s.categoria.cantidad - cant_total) > 1.0 :
                return True 
            else:
                return False
            
def chequear_cantidad(request, producto, cantidad_carro):
    productos_stock = Producto.objects.all()   
    valor = True
    cant_total = total_prod_pedido(request, producto, valor)  
    print(producto)
    print(producto.categoria)
    carro=Carro(request)
    print(carro.carro["datos"]["tipo"])
    print(type(carro.carro["datos"]["tipo"]))

    for p_s in productos_stock:
        # print(p_s)
        # print(f"Stock Prod: {p_s.stock}, Stock Cat: {p_s.categoria.stock}")
        # print(f"Cantid Prod: {p_s.cantidad} > Cantid Carro {cantidad_carro}")
        # print(f"Cantid Cat: {p_s.categoria.cantidad} > Cantid Carro {cantidad_carro}")
        # print(f"Cantid Cat: {p_s.categoria.cantidad} - cant_total {cant_total} = {p_s.categoria.cantidad - cant_total}")
        if p_s.id == producto.id:            
            
            if producto.categoria == "Pizzas" and (p_s.categoria.cantidad - cant_total) >= 0.5:
                valor2= True
            elif producto.categoria != "Pizzas" and (p_s.categoria.cantidad - cant_total) >= 1:
                valor2= True
            else:
                valor2= False            
            print(f"Valor2: {valor2}")
            if carro.carro["datos"]["tipo"] == 0:
                if p_s.stock and p_s.categoria.stock and p_s.cantidad > cantidad_carro and p_s.categoria.cantidad > cantidad_carro and valor2:
                    return True 
                else:
                    return False        
            else:
                if p_s.stock and p_s.categoria.stock and p_s.cantidad > cantidad_carro and p_s.categoria.cantidad > cantidad_carro and valor2:
                    return True 
                else:
                    return False        

def chequear_actualizacion(request, producto, nueva_cantidad):
    productos_stock = Producto.objects.all()  
    valor = False         
    cant_total = total_prod_pedido(request, producto, valor)
    
    for p_s in productos_stock:
        # print(p_s)
        # print(f"Stock Prod: {p_s.stock}, Stock Cat: {p_s.categoria.stock}")
        # print(f"Cantid Prod: {p_s.cantidad} >= Nueva cantidad: {nueva_cantidad}")
        # print(f"Cantid Cat: {p_s.categoria.cantidad} >= Nueva cantidad: {nueva_cantidad}")
        # print(f"Cantid Cat: {p_s.categoria.cantidad} >= cant_total {cant_total} + nueva_cantidad {nueva_cantidad}: {cant_total + nueva_cantidad}")
        if p_s.id == producto.id:
            if p_s.stock and p_s.categoria.stock and p_s.cantidad >= nueva_cantidad and p_s.categoria.cantidad >= nueva_cantidad and p_s.categoria.cantidad >= cant_total + nueva_cantidad:
                return True 
            else:
                return False               
   
    
def total_prod_pedido(request, producto, valor):
    carro = Carro(request)
    cat = str(producto.categoria)
    cant_total = 0
        
    if valor:
        for key, value in carro.carro.items():
            if key not in ["datos", "empanadas"]:
                if value.get("categoria") == cat:
                    cant_total += float(value.get("cantidad", 0))
        return cant_total  
    else:           
        for key, value in carro.carro.items():
            if key not in ["datos", "empanadas"]:
                if value.get("categoria") == cat  and value.get("nombre") != producto.nombre:
                    cant_total += float(value.get("cantidad", 0))
        return cant_total
      
def recheq_stock_pedido(request):
    carro = Carro(request)
    productos_stock = Producto.objects.all()  
    print("ENTRO A LA FUNCION")
    for key, value in carro.carro.items():
        if key not in ["datos", "empanadas"]:
            for producto in productos_stock:
                if value.get("cantidad") > producto.cantidad:
                    #AQUI QUIERO VOLVER AL CARRO PARA CORREGIR LA CANTIDAD
                    print("EL STOCK NOOOO ES SUFICIENTE")
                    return False
                else:
                    print("EL STOCK ES SUFICIENTE")
                    return True


    return True