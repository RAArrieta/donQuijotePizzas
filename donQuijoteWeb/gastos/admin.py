from django.contrib import admin
from .models import Proveedores, Insumos

admin.site.register([Proveedores, Insumos])