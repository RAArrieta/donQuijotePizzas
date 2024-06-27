from django.urls import path
from . import views

app_name="pedido"

urlpatterns = [
    path('', views.procesar_ped, name="procesar_ped")
]