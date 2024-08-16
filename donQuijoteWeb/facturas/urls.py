from django.urls import path
from . import views

app_name="facturas"

urlpatterns = [
    path('', views.home, name="home"),
    path('abrir_caja/', views.abrir_caja, name="abrir_caja"),
    path('cerrar_caja/', views.cerrar_caja, name="cerrar_caja"),
]