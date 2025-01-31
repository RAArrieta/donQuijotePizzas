from django.db import models
from django.utils.timezone import now
from costos.models import Proveedores
   
class Gastos(models.Model):
    ESTADO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('mercado', 'Mercado'),
        ('naranja', 'Naranja'),
    ]
    proveedor=models.ForeignKey(Proveedores, on_delete=models.CASCADE, verbose_name="Proveedor")
    monto=models.FloatField(verbose_name="Monto")
    fecha = models.DateField(default=now)
    forma_pago = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    
    def __str__(self):
        return self.proveedor.nombre
