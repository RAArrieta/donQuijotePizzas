from django.db import models

class ProductoCategoria(models.Model):
    nombre=models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre=models.CharField(max_length=50, verbose_name="Nombre")
    categoria=models.ForeignKey(ProductoCategoria, on_delete=models.CASCADE, verbose_name="Categoría")
    descripcion=models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción")
    precio_unit=models.FloatField(verbose_name="P. Unitario")
    precio_media=models.FloatField(blank=True, null=True, verbose_name="P. Media")
    precio_doc=models.FloatField(blank=True, null=True, verbose_name="P. Docena")
    
    def __str__(self):
        return self.nombre