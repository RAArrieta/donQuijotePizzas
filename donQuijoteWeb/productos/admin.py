from django.contrib import admin
from .models import Producto, ProductoCategoria, Proveedores, Insumos

class ProductoAdmin(admin.ModelAdmin):
    list_display=("nombre", "precio_unit", "precio_media", "precio_doc")
    search_fields=("nombre",)
    list_filter=("categoria",)

admin.site.register(Producto, ProductoAdmin)
admin.site.register(ProductoCategoria)
admin.site.register([Proveedores, Insumos])
