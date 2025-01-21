from django.urls import path
from . import views

app_name="gastos"

urlpatterns = [
    path('', views.home, name="home"),
    path("listar_insumos/", views.listar_insumos, name="listar_insumos"),
    path("listar_proveedores/", views.listar_proveedores, name="listar_proveedores"),
    path("insumos_create/", views.InsumosCreate.as_view(), name="insumos_create"),
    path("proveedor_create/", views.ProveedoresCreate.as_view(), name="proveedor_create"),
    path("insumos_update/<int:pk>", views.InsumosUpdate.as_view(), name="insumos_update"),
    path("proveedores_update/<int:pk>", views.ProveedoresUpdate.as_view(), name="proveedores_update"),
]