from django.contrib import admin
from .models import Proveedores, Insumos, Gastos

admin.site.register([Proveedores, Insumos, Gastos])