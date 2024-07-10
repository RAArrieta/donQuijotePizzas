from django.db import models
from productos.models import Producto
from django.db.models import F, Sum, FloatField

# Create your models here.

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('entregado', 'Entregado'),
        ('pendiente', 'Pendiente'),
        ('cancelado', 'Cancelado')
    ]

    PAGO_CHOICES = [
        ('efectivo', 'EFT'),
        ('mercado', 'MP'),
        ('naranja', 'NRJ'),
        ('debito', 'DEBIT'),
        ('cobrar', 'COBRAR')
    ]
    
    FORMA_ENTREGA_CHOICES = [
        ('retira', 'Retira'),
        ('envio', 'Envio'),
    ]
    
    estado=models.CharField(max_length=10, choices=ESTADO_CHOICES)
    pago=models.CharField(max_length=10, choices=PAGO_CHOICES)
    forma_entrega=models.CharField(max_length=10, choices=FORMA_ENTREGA_CHOICES)
    hora=models.DateTimeField(auto_now_add=True)
    nombre=models.CharField(max_length=50, blank=True, null=True)
    direccion=models.CharField(max_length=100, blank=True, null=True)
    observacion=models.CharField(max_length=100, blank=True, null=True)
    
    
    def __str__(self):
        return f"Pedido: {self.id}"
    
    @property
    def total(self):
        pass
        # return self.pedidoproducto_set.aggregate(
        #     total=Sum(F("precio")*F("cantidad"), output_field=FloatField())
        # ),["total"]
    
    class Meta:
        db_table="pedidos"
        verbose_name="Pedido"
        verbose_name_plural="Pedidos"
        ordering=["id"]
        
class PedidoProductos(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido=models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad=models.FloatField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.cantidad} {self.producto.nombre}"
    
    class Meta:
        db_table="productospedidos"
        verbose_name="Producto pedido"
        verbose_name_plural="Productos pedidos"
        ordering=["id"]