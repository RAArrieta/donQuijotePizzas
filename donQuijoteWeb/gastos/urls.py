from django.urls import path
from . import views

app_name="gastos"

urlpatterns = [
    path('', views.home, name="home"),
]