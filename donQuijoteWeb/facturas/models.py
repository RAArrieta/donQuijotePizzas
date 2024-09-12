from django.db import models
from productos.models import Producto

class Facturas(models.Model):
    forma_pago = models.CharField(max_length=50)
    pago = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    envio = models.FloatField(null=True, blank=True)
        
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
    estado_caja = models.BooleanField()