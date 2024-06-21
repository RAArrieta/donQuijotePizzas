from django.urls import path
from . import views

app_name="carro"

urlpatterns = [
    path('', views.home, name='home'),
    path('carro/', views.carro, name='carro'),
]