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
                    "estado": "",
                    "pago": "",
                    "forma_entrega": "envio",
                    "nombre": "",
                    "direccion": "",
                    "observacion": "",
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
                "cantidad": float(1.0),
                "subtotal": float(producto.precio_unit),  
                "categoria": str(producto.categoria)
            }
        else:
            for key, value in self.carro.items():
                if key == producto_id_str:
                    if value["precio_media"] != "None" and value["precio_doc"] == "None":
                        value["cantidad"] = float(value["cantidad"]) + 0.5
                    else:
                        value["cantidad"] = float(value["cantidad"]) + 1.0
                    break
        self.guardar_carro()
        
    def restar_producto(self, producto):
        producto_id_str = str(producto.id)
        for key, value in self.carro.items():
            if key == producto_id_str:
                if value["precio_media"] != "None" and value["precio_doc"] == "None":
                    restar=0.5   
                else:
                    restar=1.0
                value["cantidad"] = float(value["cantidad"]) - restar   
                
                if value["precio_media"] != "None" and value["precio_doc"] == "None":
                    minimo=0.5
                else:
                    minimo=1.0
                if value["cantidad"] < minimo:
                    self.eliminar(producto)
                    break
        self.guardar_carro()
        
    def actualizar_cant(self, producto, nueva_cantidad):
        producto_id = str(producto.id)
        self.carro[producto_id]['cantidad'] = float(nueva_cantidad)
        self.guardar_carro()
        
        

    def eliminar(self, producto):
        producto_id_str = str(producto.id)
        if producto_id_str in self.carro:
            del self.carro[producto_id_str]
            self.guardar_carro()
    
    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True
        
    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True
        print(f"Carro guardado: {self.carro}")
        
        
    
    # def guardar_carro(self):
    #     self.session["carro"] = self.carro
    #     self.session.modified = True

    def agregar_datos(self, datos):
        if "nombre" in datos:
            self.carro["datos"]["nombre"]=datos["nombre"]
        if "direccion" in datos:
            self.carro["datos"]["direccion"]=datos["direccion"]
        if "observacion" in datos:
            self.carro["datos"]["observacion"]=datos["observacion"]
        if "estado" in datos:
            self.carro["datos"]["estado"]=datos["estado"]
        if "pago" in datos:
            self.carro["datos"]["pago"]=datos["pago"]
        if "forma_entrega" in datos:
            self.carro["datos"]["forma_entrega"]=datos["forma_entrega"]
        self.guardar_carro()
        
    def comprobacion_pedido(self):
        comprobacion_pedido=False
        if self.carro["datos"]["direccion"] != "" and len(self.carro.keys()) > 1: 
            comprobacion_pedido=True
        return comprobacion_pedido
    

    
    def calcular_precio(self):
        pass