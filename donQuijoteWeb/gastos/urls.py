from django.urls import path
from . import views

app_name="gastos"

urlpatterns = [
    path('', views.home, name="home"),
    path("cargar_pagos/", views.cargar_pagos, name="cargar_pagos"),
    path('eliminar_pago/<int:gasto_id>/', views.eliminar_pago, name='eliminar_pago'),
]