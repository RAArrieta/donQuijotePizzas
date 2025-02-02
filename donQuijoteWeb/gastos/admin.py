from django.contrib import admin
from .models import Gastos

class GastosAdmin(admin.ModelAdmin):
    list_display = ("formas_pago", "monto", "fecha")
    list_filter = ("forma_pago", ("fecha", admin.DateFieldListFilter)) 
    ordering = ("id",)
    search_fields = ['fecha']  
    
    def formas_pago(self, obj):
        return obj.forma_pago.capitalize()

admin.site.register(Gastos, GastosAdmin)