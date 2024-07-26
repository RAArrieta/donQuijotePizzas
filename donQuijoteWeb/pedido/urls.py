from django.urls import path
from . import views

app_name="pedido"

urlpatterns = [
    path('', views.home, name="home"),
    path('procesar_ped/', views.procesar_ped, name="procesar_ped")
]

urlpatterns += [
     path("formaentrega_update/<int:pk>", views.FormaEntregaUpdate.as_view(), name="formaentrega_update"),
]