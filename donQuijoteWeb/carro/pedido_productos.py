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
                "datos":{
                    "estado": "Pendiente",
                    "pago": "Cobrar",
                    "forma_entrega": "Retira",
                    "nombre": "nombre",
                    "direccion": "direccion",
                    "observacion": "observacion",
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
        else:
            for key, value in self.carro.items():
                if key == producto_id_str:
                    value["cantidad"] += 1
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
    
    def agregar_datos(self, datos):
        self.carro["datos"] = {
            "nombre": datos["nombre"],
            "direccion": datos["direccion"],
            "observacion": datos["observacion"]
        }
        self.guardar_carro()
    
    
    
    
    # def agregar_datos(self, datos):
    #     dato = datos
    #     print(dato)
    #     for key, value in self.carro.items():
    #         if key == "datos":
    #             self.datos = {
    #                 # "estado": estado,
    #                 # "pago": pago,
    #                 "nombre": value["nombre"],
    #                 "direccion": value["direccion"],
    #                 "observacion": value["observacion"]
    #             }
    #     self.guardar_datos()

    # def guardar_datos(self):
    #     self.session["datos"] = self.datos
    #     self.session.modified = True

    # def obtener_datos(self, id_datos):
    #     return self.datos.get(id_datos, None)

    # def eliminar_datos(self, id_datos):
    #     if id_datos in self.datos:
    #         del self.datos[id_datos]
    #         self.guardar_datos()

    # def actualizar_datos(self, id_datos, estado=None, pago=None, nombre=None, direccion=None, observacion=None):
    #     datos = self.datos.get(id_datos)
    #     if datos:
    #         if estado:
    #             datos["estado"] = estado
    #         if pago:
    #             datos["pago"] = pago
    #         if nombre:
    #             datos["nombre"] = nombre
    #         if direccion:
    #             datos["direccion"] = direccion
    #         if observacion:
    #             datos["observacion"] = observacion
    #         self.guardar_datos()


