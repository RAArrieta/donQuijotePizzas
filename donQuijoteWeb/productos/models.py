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
        
class ProductoCategoria(models.Model):
    nombre=models.CharField(max_length=50)
    estado=models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre=models.CharField(max_length=50, verbose_name="Nombre")
    categoria=models.ForeignKey(ProductoCategoria, on_delete=models.CASCADE, verbose_name="Categoría")
    descripcion=models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción")
    precio_unit=models.FloatField(verbose_name="P. Unitario")
    precio_media=models.FloatField(blank=True, null=True, verbose_name="P. Media")
    precio_doc=models.FloatField(blank=True, null=True, verbose_name="P. Docena")
    precio_rec = models.FloatField(default=1, verbose_name="Precio Recomendado")

    def __str__(self):
        return self.nombre

class ProductoInsumos(models.Model):
    ESTADO_CHOICES = [
        ('Gr', 'Gr'),
        ('Ltr', 'Ltr'),
        ('Unid', 'Unid'),
        ('Doc', 'Doc'),
        ('Caja', 'Caja'),
        ('Lata', 'Lata'),
        ('Rollo', 'Rollo'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto", related_name="insumos")
    insumo = models.ForeignKey(Insumos, on_delete=models.CASCADE, verbose_name="Insumo")
    cantidad = models.FloatField(default=1, verbose_name="Cantidad")
    unidad=models.CharField(default='Gr',max_length=50, choices=ESTADO_CHOICES)

    def __str__(self):
        return f"{self.producto.nombre} - {self.insumo.nombre}: {self.cantidad} {self.unidad}"