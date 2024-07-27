from productos.models import Producto

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
                    "precio_entrega": 0.0,
                    "envio":True,
                    "nombre": "",
                    "direccion": "",
                    "observacion": "",
                    "total":0.0,
                },
                "empanadas": {
                    "cantidad":"",
                    "subtotal_emp":0.0,
                }
            }
        self.carro = carro
        
    def agregar(self, producto):
        producto_id_str = str(producto.id)
        if producto_id_str not in self.carro.keys():
            self.carro[producto_id_str] = {
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
                        sumar = 0.5
                    else:
                        sumar = 1.0
                    value["cantidad"] = float(value["cantidad"]) + sumar
                    break
        
        self.calcular_precio()
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
                self.calcular_precio()
                
                if value["precio_media"] != "None" and value["precio_doc"] == "None":
                    minimo=0.5
                else:
                    minimo=1.0
                if value["cantidad"] < minimo:
                    self.eliminar(producto)
                    self.calcular_precio()
                    break
        self.guardar_carro()
        
    def actualizar_cant(self, producto, nueva_cantidad):
        producto_id = str(producto.id)
        self.carro[producto_id]['cantidad'] = float(nueva_cantidad)
        self.calcular_precio()
        self.guardar_carro()
              
    def eliminar(self, producto):
        producto_id_str = str(producto.id)
        if producto_id_str in self.carro:
            del self.carro[producto_id_str]
            self.guardar_carro()
            self.calcular_precio() 
    
    def limpiar_carro(self):
        self.session["carro"] = {}
        self.session.modified = True
        
    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True

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
            self.carro["datos"]["precio_entrega"]=datos["precio_entrega"]
            self.carro["datos"]["envio"]=bool(datos["envio"])
        self.guardar_carro()
        
    def comprobacion_pedido(self):
        comprobacion_pedido=False
        if self.carro["datos"]["direccion"] == "" and self.carro["datos"]["envio"] == False and len(self.carro.keys()) > 2: 
            comprobacion_pedido=True
        elif self.carro["datos"]["direccion"] != "" and self.carro["datos"]["envio"] == True and len(self.carro.keys()) > 2: 
            comprobacion_pedido=True
        return comprobacion_pedido
    
    
    def cantidad_empanadas(self):
        cantidad_empanadas=0
        for key, value in self.carro.items():
            if key != "datos" and key != "empanadas" and value["precio_doc"] != "None":
                cantidad_empanadas += value["cantidad"]
        return cantidad_empanadas
       
    def calcular_precio(self):
        cantidad_empanadas = float(self.cantidad_empanadas())
        self.session["carro"]["empanadas"]["cantidad"] = cantidad_empanadas 
        subtotal_emp = 0.0
        
        for key, value in self.carro.items():
            if key != "datos" and key != "empanadas":
                if value["precio_unit"] != "None" and value["precio_media"] == "None" and value["precio_doc"] == "None":
                    value["subtotal"] = float(value["cantidad"]) * float(value["precio_unit"])

                
                if value["precio_media"] != "None" and value["precio_doc"] == "None":
                    if value["cantidad"] < 1.0:
                        media=0.5
                    else:
                        media = float(value["cantidad"]) % int(value["cantidad"])
                    entero = int(value["cantidad"])
                    
                    if value["cantidad"] < 1.0:
                        value["subtotal"] = float(value["precio_media"])
                    elif media != 0 and value["cantidad"] > 1:
                        value["subtotal"] = (entero * float(value["precio_unit"])) + float(value["precio_media"])
                    else:
                        value["subtotal"] = float(value["cantidad"]) * float(value["precio_unit"])

            
                
                
                   
                if value["precio_doc"] != "None":
                    
                    precio_unit = float(value["precio_unit"])
                    precio_media = float(value["precio_media"])
                    precio_doc = float(value["precio_doc"])

                    if cantidad_empanadas == 0.0:
                        subtotal_emp = 0.0
                    if cantidad_empanadas < 6.0:
                        subtotal_emp = cantidad_empanadas * precio_unit
                    elif cantidad_empanadas < 12.0:
                        resto = cantidad_empanadas % 6.0
                        if resto == 0.0:
                            subtotal_emp = precio_media
                        else:
                            subtotal_emp = precio_media + (resto * precio_unit)
                    else:
                        docenas = cantidad_empanadas // 12.0
                        sueltas = cantidad_empanadas % 12.0
                        if sueltas == 0.0:
                            subtotal_emp = precio_doc * docenas
                        elif sueltas < 6.0:
                            subtotal_emp = (precio_doc * docenas) + (sueltas * precio_unit)
                        elif sueltas == 6.0:
                            subtotal_emp = (precio_doc * docenas) + (precio_doc / 2.0)
                        else:
                            resto = sueltas - 6.0
                            subtotal_emp = (precio_doc * docenas) + (precio_doc / 2.0) + (resto * precio_unit)
                
        self.session["carro"]["empanadas"]["subtotal_emp"] = float(subtotal_emp)
        self.guardar_carro()
        
    def importe_total_carro(self):
        total = 0.0
        for key, value in self.carro.items():
            if key != "datos" and key != "empanadas" and value["precio_doc"] == "None":
                total = float(total)+float(value["subtotal"])
            elif key == "datos" and value["precio_entrega"] != None:
                total = float(total)+float(value["precio_entrega"])
            elif key == "empanadas":
                total = float(total)+float(value["subtotal_emp"])
        
        self.session["carro"]["datos"]["total"] = float(total)
        return total