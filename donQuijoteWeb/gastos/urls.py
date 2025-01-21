from django.urls import path
from . import views

app_name="gastos"

urlpatterns = [
    path('', views.home, name="home"),
    path("create/", views.InsumosCreate.as_view(), name="insumos_create"),
]