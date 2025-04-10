from django.urls import path
from . import views

app_name="pedido"

urlpatterns = [
    path('', views.listar_pedidos, name="home"),
    path('pendientes/', views.listar_pendientes, name="listar_pendientes"),
    path('entregados/', views.listar_entregados, name="listar_entregados"),
    path('reservados/', views.listar_reservados, name="listar_reservados"),
    path('procesar_ped/', views.procesar_ped, name="procesar_ped"),
    path('modificar/pedido/<str:tipo>/<int:pedido>', views.modificar_pedido, name="modificar_pedido")
]

urlpatterns += [
     path("formaentrega_update/<int:pk>", views.FormaEntregaUpdate.as_view(), name="formaentrega_update"),
]