from django.db import models
from productos.models import Producto
from django.utils.timezone import now

class Facturas(models.Model):
    forma_pago = models.CharField(max_length=50)
    pago = models.FloatField()
    fecha = models.DateField(default=now)
    envio = models.BooleanField(default=True) 
    turno = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        db_table = "facturas"
        verbose_name = "Facturas"
        
    def __str__(self):
        return f"Factura {self.id}"

class FacturaProducto(models.Model):
    factura = models.ForeignKey(Facturas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.FloatField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Factura {self.factura.id}"

class Caja(models.Model):
    TURNOS = [
        ("mediodia", "Mediodía"),
        ("noche", "Noche"),
    ]

    estado_caja = models.BooleanField(default=False)
    turno = models.CharField(max_length=20, choices=TURNOS, null=True, blank=True)

    