from pedido.models import PedidoProductos, PedidosProductosReservados
from productos.models import Producto
from .carro import Carro

def chequear_stock(request, producto, cantidad_producto_carro):
    print("def chequear_stock(request, producto)")
    """
    Se usa cuando el producto NO está en el carrito
    """
    carro = Carro(request)
    categoria = producto.categoria
    
    cantidad_producto_carro = 1.0
    
    total_categoria = float(cantidad_categoria_en_carro(request, categoria, carro))
    
    stock_producto_disponible = producto.cantidad
    stock_categoria_disponible = producto.categoria.cantidad
    
    # print(f"Total categoria: {total_categoria}")
    # print(f"stock_producto_disponible: {stock_producto_disponible}")
    # print(f"stock_categoria_disponible: {stock_categoria_disponible}")   
    # print(f"cantidad_producto_carro: {cantidad_producto_carro}")  

        
    return (
        producto.stock 
        and producto.categoria.stock 
        
        and stock_categoria_disponible >= total_categoria
        and stock_categoria_disponible >= cantidad_producto_carro
        and stock_producto_disponible >= cantidad_producto_carro
    )
  
    
def chequear_cantidad(request, producto, cantidad_producto_carro):
    print("def chequear_cantidad(request, producto, cantidad_producto_carro)")
    """
    Se usa cuando el producto ya está en el carrito y se presiona +
    """
    carro = Carro(request)
    categoria = producto.categoria
    
    total_categoria = float(cantidad_categoria_en_carro2(request, categoria, carro))
    
    stock_producto_disponible = producto.cantidad
    
    stock_categoria_disponible = producto.categoria.cantidad
    
    # print(f"Total categoria: {total_categoria}")
    # print(f"stock_producto_disponible: {stock_producto_disponible}")
    # print(f"stock_categoria_disponible: {stock_categoria_disponible}")   
    # print(f"cantidad_producto_carro: {cantidad_producto_carro}")

    # print(f"stock_categoria_disponible - cantidad_producto_carro >= 0.5: {stock_categoria_disponible - cantidad_producto_carro >= 0.5}")
    # print(f"stock_producto_disponible - cantidad_producto_carro >= 0.5: {stock_producto_disponible - cantidad_producto_carro >= 0.5}")
    
    # print(f"stock_categoria_disponible - cantidad_producto_carro >= 1: {stock_categoria_disponible - cantidad_producto_carro >= 1}")
    # print(f"stock_producto_disponible - cantidad_producto_carro >= 1: {stock_producto_disponible - cantidad_producto_carro >= 1}")

    if str(producto.categoria) == "Pizzas":
        
        return (
            producto.stock
            and producto.categoria.stock
            
            and stock_categoria_disponible - cantidad_producto_carro >= 0.5 
            and stock_producto_disponible - cantidad_producto_carro >= 0.5  
            
            and stock_categoria_disponible >= total_categoria 
            and stock_categoria_disponible >= cantidad_producto_carro 
        )
    else:
        return (
            producto.stock 
            and producto.categoria.stock
            
            and stock_categoria_disponible - cantidad_producto_carro >= 1
            and stock_producto_disponible - cantidad_producto_carro >= 1  
            
            and stock_categoria_disponible >= total_categoria 
            and stock_categoria_disponible >= cantidad_producto_carro

        )
                
def cantidad_categoria_en_carro(request, categoria, carro):
    """
    Devuelve la cantidad TOTAL de una categoría
    sumando TODOS los productos del carrito
    """
    total_categoria = 1.0
    
    for key, item in carro.carro.items():
        if key in ["datos", "empanadas"]:
            continue

        producto_carro = Producto.objects.get(id=int(key))

        if producto_carro.categoria == categoria:
            total_categoria += float(str(item["cantidad"]))
    
    return total_categoria


def cantidad_categoria_en_carro2(request, categoria, carro):
    """
    Devuelve la cantidad TOTAL de una categoría
    sumando TODOS los productos del carrito
    """
    if str(categoria) == "Pizzas":
        total_categoria = 0.5
    else:
        total_categoria = 1.0
    
    for key, item in carro.carro.items():
        if key in ["datos", "empanadas"]:
            continue

        producto_carro = Producto.objects.get(id=int(key))

        if producto_carro.categoria == categoria:
            total_categoria += float(str(item["cantidad"]))
    
    return total_categoria




def chequear_actualizacion(request, producto, nueva_cantidad):
    print("def chequear_actualizacion(request, producto, nueva_cantidad)")
    """
    Se usa SOLO cuando se edita un producto existente
    """
    carro = Carro(request)
    categoria = producto.categoria
    
    #CANTIDAD DEL PRODUCTO EXISTENTE EN CARRO  
    vieja_cantidad = prueba_buscar_cantidad(request, carro, producto)   
    
    #CANTIDAD DE CATEGORIA (SUMA DE PROD EN CAT) EXISTENTE EN CARRO
    total_categoria = float(cantidad_categoria_en_carro3(request, categoria, carro)) - vieja_cantidad
        
    #STOCK DISPONIBLE 
    stock_producto_disponible = producto.cantidad
    stock_categoria_disponible = producto.categoria.cantidad
    
    # print("*************************************************************")
    # print("*************************************************************")
    # print(f"Nueva cantidad: {nueva_cantidad}")
    # print(f"vieja_cantidad: {vieja_cantidad}")
    # print(f"Total categoria: {total_categoria}")
    # print(f"Producto cantidad: {stock_producto_disponible}") 
    # print(f"Categoria cantidad: {stock_categoria_disponible}")   
    # print("*************************************************************")
    # print("*************************************************************")   

    return (
        producto.stock
        and producto.categoria.stock
        
        and stock_producto_disponible >= nueva_cantidad - vieja_cantidad
        and stock_categoria_disponible >= nueva_cantidad - vieja_cantidad
        and stock_categoria_disponible >= total_categoria + nueva_cantidad
    )
    



def prueba_buscar_cantidad(request, carro, producto):
    cant_vieja = 0.0
    
    for key, item in carro.carro.items():
        if key in ["datos", "empanadas"]:
            continue
        
        producto_carro = Producto.objects.get(id=int(key))
        print(producto_carro)
        
        # comparar PRODUCTO con PRODUCTO
        if producto_carro == producto:
            cant_vieja = float(item["cantidad"])
            break  # ya lo encontramos, no seguimos
    
   
    return cant_vieja



def cantidad_categoria_en_carro3(request, categoria, carro):
    """
    Devuelve la cantidad TOTAL de una categoría
    sumando TODOS los productos del carrito
    """
    total_categoria = 0.0
    
    for key, item in carro.carro.items():
        if key in ["datos", "empanadas"]:
            continue

        producto_carro = Producto.objects.get(id=int(key))

        if producto_carro.categoria == categoria:
            total_categoria += float(str(item["cantidad"]))
    
    return total_categoria



