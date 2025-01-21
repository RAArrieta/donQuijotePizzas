from django.db import models

from django.db import models

class Proveedores(models.Model):
    nombre=models.CharField(max_length=50)
    estado=models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
class Insumos(models.Model):
    ESTADO_CHOICES = [
        ('Kg', 'Kg'),
        ('Gr', 'Gr'),
        ('Ltr', 'Ltr'),
        ('Unid', 'Unid'),
        ('Doc', 'Doc'),
        ('Caja', 'Caja'),
        ('Pack', 'Pack'),
        ('Lata', 'Lata'),
        ('Rollo', 'Rollo'),
    ]
    nombre=models.CharField(max_length=50, verbose_name="Nombre")
    proveedor=models.ForeignKey(Proveedores, on_delete=models.CASCADE, verbose_name="Proveedor")
    
    precio=models.FloatField(verbose_name="Precio")
    unidad=models.CharField(max_length=50, choices=ESTADO_CHOICES)

    
    def __str__(self):
        return self.nombre
