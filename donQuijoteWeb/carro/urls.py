from django.urls import path
from . import views

app_name="carro"

urlpatterns = [
    path('', views.home, name='home'),
    path('carro/', views.carro, name='carro'),
    path('agregar/<int:producto_id>/', views.agregar_producto, name='agregar'),
    path('agregar_datos/', views.agregar_datos, name='agregar_datos'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar'),
    path('restar/<int:producto_id>/', views.restar_producto, name='restar'),
    path('limpiar/', views.limpiar_carro, name='limpiar'),
]