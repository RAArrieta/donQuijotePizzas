from django.urls import path
from . import views

app_name="pedido"

urlpatterns = [
    path('', views.listar_pedidos, name="home"),
    path('procesar_ped/', views.procesar_ped, name="procesar_ped"),
    path('modificar/pedido/<int:pedido>', views.modificar_pedido, name="modificar_pedido")
]

urlpatterns += [
     path("formaentrega_update/<int:pk>", views.FormaEntregaUpdate.as_view(), name="formaentrega_update"),
]