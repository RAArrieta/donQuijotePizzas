from django.urls import path
from . import views

app_name="facturas"

urlpatterns = [
    path('', views.home, name="home"),
    path('abrir_caja/', views.abrir_caja, name="abrir_caja"),
    path('cerrar_caja/', views.cerrar_caja, name="cerrar_caja"),
    path('facturas/', views.facturas, name="facturas"),
    path('facturas_detalle/', views.facturas_detalle, name="facturas_detalle"),
    path('imprimir-facturas/', views.imprimir_facturas, name='imprimir_facturas'),
]