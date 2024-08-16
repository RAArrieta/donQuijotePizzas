from django.db import models

class Facturas(models.Model):
    forma_pago = models.CharField(max_length=50)
    pago = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
        
    class Meta:
        db_table = "facturas"
        verbose_name = "Facturas"
        
    def __str__(self):
        return f"Factura {self.id}"
        
class Caja(models.Model):
    estado_caja = models.BooleanField()