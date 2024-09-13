from django.urls import path
from . import views

app_name="estadisticas"

urlpatterns = [
    path('', views.home, name="home"),
]