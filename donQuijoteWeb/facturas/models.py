from django.db import models

class Facturas(models.Model):
    efectivo = models.FloatField()
    mercado = models.FloatField()
    naranja = models.FloatField()
    
    caja_inicial = models.FloatField()
    caja_efectivo = models.FloatField()
    caja_mercado = models.FloatField()
    caja_naranja = models.FloatField()
    caja_total = models.FloatField()
    
    estado_caja = models.BooleanField()
    
    def __str__(self):
        return f"Caja diaria Total: {self.caja_total}"
    
    class Meta:
        db_table = "facturas"
        verbose_name = "Facturas"
