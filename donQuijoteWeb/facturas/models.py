from django.db import models
from productos.models import Producto
from pedido.models import Pedido
from django.utils.timezone import now

class Facturas(models.Model):
    pedido = models.CharField(max_length=20, blank=True, null=True)
    forma_pago = models.CharField(max_length=50)
    pago = models.FloatField()
    descuento = models.CharField(max_length=50)
    fecha = models.DateField(default=now)
    envio = models.BooleanField(default=True) 
    turno = models.CharField(max_length=20, null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        db_table = "facturas"
        verbose_name = "Facturas"
        
    def __str__(self):
        return f"Factura {self.id}"

class FacturaProducto(models.Model):
    factura = models.ForeignKey(Facturas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    empanadas = models.CharField(max_length=20, null=True, blank=True)
    cantidad = models.FloatField()
    subtotal = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Factura {self.factura.id}"

class Caja(models.Model):
    TURNOS = [
        ("mediodia", "Mediodía"),
        ("noche", "Noche"),
    ]

    estado_caja = models.BooleanField(default=False)
    turno = models.CharField(max_length=20, choices=TURNOS, null=True, blank=True)

    