from django.urls import path
from . import views

app_name="carro"

urlpatterns = [
    path('', views.carro, name='carro'),
    path('nuevo/producto/<int:producto_id>/', views.nuevo_producto, name='nuevo_producto'),
    path('cargar/datos/', views.cargar_datos, name='cargar_datos'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar'),
    path('restar/<int:producto_id>/', views.restar_producto, name='restar'),
    path('actualizar/cantidad/<int:producto_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar'),
    path('limpiar/', views.limpiar_carro, name='limpiar'),
]