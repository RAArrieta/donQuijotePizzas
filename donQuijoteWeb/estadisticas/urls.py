from django.urls import path
from . import views

app_name="estadisticas"

urlpatterns = [
    path('', views.home, name="home"),
    path('cargar_datos/', views.cargar_datos, name="cargar_datos"),
]