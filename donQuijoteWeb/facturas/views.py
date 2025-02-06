from django.shortcuts import render

from .caja import listar_caja, abrirCaja, cerrarCaja
from .facturas import cargar_fact, listar_facturas

def home(request):
    return listar_caja(request)

def abrir_caja(request):
    return abrirCaja(request)

def cerrar_caja(request):
    return cerrarCaja(request)

def facturas(request):
    return listar_facturas(request)