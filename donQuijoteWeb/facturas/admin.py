from django.contrib import admin
from .models import Facturas, Caja

class FacturasAdmin(admin.ModelAdmin):
    list_display = ("nro_factura", "formas_pago", "pago")
    list_filter = ("forma_pago", "fecha")
    ordering = ("id",) 

    def nro_factura(self, obj):
        return f"Factura {obj.id}"
    
    def formas_pago(self, obj):
        return obj.forma_pago.capitalize()

    
admin.site.register(Facturas, FacturasAdmin)
admin.site.register(Caja)
