from productos.models import Producto

def select_productos():
    productos = Producto.objects.all()
    categorias = {}
    for producto in productos:
        if producto.categoria not in categorias:
            categorias[producto.categoria] = []
        categorias[producto.categoria].append(producto)
        
    return categorias

class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            carro = self.session["carro"] = {
                "contador_empanadas": {
                    "cantidad": 0,
                    "subtotal": 0.0
                }
            }
        self.carro = carro

    def agregar(self, producto):
        producto_id_str = str(producto.id)
        if producto_id_str not in self.carro.keys():
            self.carro[producto.id] = {
                "producto_id": producto.id,
                "nombre": producto.nombre,
                "precio_unit": str(producto.precio_unit),
                "precio_media": str(producto.precio_media),
                "precio_doc": str(producto.precio_doc),
                "cantidad": 1,
                "subtotal": float(producto.precio_unit),  
                "categoria": str(producto.categoria)
            }
            if producto.precio_doc is not None:
                self.carro["contador_empanadas"]["cantidad"] += 1
        else:
            for key, value in self.carro.items():
                if key == producto_id_str:
                    value["cantidad"] += 1
                    if producto.precio_doc is not None:
                        self.carro["contador_empanadas"]["cantidad"] += 1
                    value["subtotal"] += producto.precio_unit
                    break
        self.guardar_carro()

    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True

    def eliminar(self, producto):
        producto_id_str = str(producto.id)
        if producto_id_str in self.carro:
            del self.carro[producto_id_str]
            self.guardar_carro()

    def restar_producto(self, producto):
        producto_id_str = str(producto.id)
        for key, value in self.carro.items():
            if key == producto_id_str:
                value["cantidad"] -= 1
                if producto.precio_doc is not None:
                    self.carro["contador_empanadas"]["cantidad"] -= 1
                value["subtotal"] -= producto.precio_unit
                if value["cantidad"] < 1:
                    self.eliminar(producto)
                break
        self.guardar_carro()

    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True

    def calcular_precio(self):
        pass
