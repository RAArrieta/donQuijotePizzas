from django.urls import path
from . import views

app_name="facturas"

urlpatterns = [
    path('', views.home, name="home"),
]