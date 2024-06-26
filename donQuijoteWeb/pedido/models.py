from django.db import models

# Create your models here.

class PedidoProductos(models.Model):
    nombre=models.CharField(max_length=50)
    cantidad=models.IntegerField()
    
    
class Pedido(models.Model):
    nro_ped=models.IntegerField()
    productos=models.ForeignKey(PedidoProductos, on_delete=models.CASCADE)