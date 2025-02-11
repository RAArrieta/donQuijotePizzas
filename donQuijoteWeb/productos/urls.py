from django.urls import path
from . import views
from .views import agregar_insumos_producto

app_name="productos"

urlpatterns = [
    path('', views.home, name='home'),
    path("create/", views.ProductosCreate.as_view(), name="productos_create"),
    path("update/<int:pk>", views.ProductoUpdate.as_view(), name="productos_update"),
]

urlpatterns += [
    path("categorias/", views.categorias, name="categorias"),
    path("categorias/create/", views.ProductoCategoriaCreate.as_view(), name="categorias_create"),
    path("categorias/update/<int:pk>", views.ProductoCategoriaUpdate.as_view(), name="categorias_update"),
]

urlpatterns += [
    path("lista_wa/", views.lista_wa, name="lista_wa"),
]

urlpatterns += [
    path("listar_insumos/", views.listar_insumos, name="listar_insumos"),
    path("listar_proveedores/", views.listar_proveedores, name="listar_proveedores"),
    path("insumos_create/", views.InsumosCreate.as_view(), name="insumos_create"),
    path("proveedor_create/", views.ProveedoresCreate.as_view(), name="proveedor_create"),
    path("insumos_update/<int:pk>", views.InsumosUpdate.as_view(), name="insumos_update"),
    path("proveedores_update/<int:pk>", views.ProveedoresUpdate.as_view(), name="proveedores_update"),
    path('producto/<int:producto_id>/insumos/', agregar_insumos_producto, name='agregar_insumos_producto'),
    path('eliminar_insumo/<int:insumo_id>/', views.eliminar_insumo, name='eliminar_insumo'),
]




