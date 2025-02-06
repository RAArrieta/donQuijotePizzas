from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date
from carro.select_productos import select_productos
from .estadisticas import Estadisticas
from productos.models import Producto
from .forms import MesAnoForm

from .estadisticas_funciones import enviar_forms, cargar_estadistica

def home(request):
    return enviar_forms(request)

def cargar_datos(request):
    return cargar_estadistica(request)