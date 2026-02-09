from django.db import models
from productos.models import Producto

class FormaEntrega(models.Model):
    forma_entrega = models.CharField(max_length=50)
    precio = models.FloatField(null=True, blank=True)
    envio = models.BooleanField()
    
    def __str__(self):
        return f"{self.forma_entrega}"
    
    class Meta:
        db_table = "formaentrega"
        verbose_name = "Forma de entrega"
    
class Descuentos(models.Model):
    descuento = models.CharField(max_length=50)
    precio = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.descuento}"
    
    class Meta:
        db_table = "descuento"
        verbose_name = "Descuento"
        
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
        ('cobrar', 'COBRAR')
    ]
    
    estado=models.CharField(max_length=10, choices=ESTADO_CHOICES)
    tipo = models.IntegerField(default=1)
    pago=models.CharField(max_length=10, choices=PAGO_CHOICES)
    forma_entrega=models.ForeignKey(FormaEntrega, on_delete=models.SET_NULL, null=True, blank=True)
    precio_entrega=models.FloatField(null=True, blank=True)
    hora=models.DateTimeField(auto_now_add=True)
    nombre=models.CharField(max_length=50, blank=True, null=True)
    direccion=models.CharField(max_length=100, blank=True, null=True)
    observacion=models.CharField(max_length=100, blank=True, null=True)
    cantidad_emp=models.FloatField(null=True, blank=True)
    subtotal_emp=models.FloatField(null=True, blank=True)
    total=models.FloatField()
    
    def __str__(self):
        return f"Pedido: {self.id}"
        
    class Meta:
        db_table="pedidos"
        verbose_name="Pedido"
        verbose_name_plural="Pedidos"
        ordering=["id"]
        
class PedidoProductos(models.Model):
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido=models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad=models.FloatField(default=1)
    subtotal=models.FloatField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.cantidad} {self.producto.nombre}"
    
    class Meta:
        db_table="productospedidos"
        verbose_name="Producto pedido"
        verbose_name_plural="Productos pedidos"
        ordering=["id"]

class PedidosReservado(models.Model):
    ESTADO_CHOICES = [
        ('reservado', 'Reservado'),
        ('entregado', 'Entregado'),
        ('pendiente', 'Pendiente'),
        ('cancelado', 'Cancelado')
    ]

    PAGO_CHOICES = [
        ('efectivo', 'EFT'),
        ('mercado', 'MP'),
        ('naranja', 'NRJ'),
        ('cobrar', 'COBRAR')
    ]

    id = models.AutoField(primary_key=True) 
    tipo = models.IntegerField(default=2)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='reservado')
    pago = models.CharField(max_length=10, choices=PAGO_CHOICES)
    forma_entrega = models.ForeignKey(FormaEntrega, on_delete=models.SET_NULL, null=True, blank=True)
    precio_entrega = models.FloatField(null=True, blank=True)
    hora = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    observacion = models.CharField(max_length=100, blank=True, null=True)
    cantidad_emp = models.FloatField(null=True, blank=True)
    subtotal_emp = models.FloatField(null=True, blank=True)
    total = models.FloatField()

    class Meta:
        db_table = "pedidos_reservados"
        verbose_name = "Pedido Reservado"
        verbose_name_plural = "Pedidos Reservados"
        ordering = ["id"]
    
    def save(self, *args, **kwargs):
        if not self.id:  
            ultimo_pedido = PedidosReservado.objects.order_by('-id').first()
            self.id = (ultimo_pedido.id + 1) if ultimo_pedido else 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pedido Reservado: {self.id}"
        
class PedidosProductosReservados(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(PedidosReservado, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=1)
    subtotal = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cantidad} {self.producto.nombre} (Reservado)"

    class Meta:
        db_table = "productos_pedidos_reservados"
        verbose_name = "Producto Pedido Reservado"
        verbose_name_plural = "Productos Pedidos Reservados"
        ordering = ["id"]
