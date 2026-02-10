

from django.shortcuts import render
from .models import Facturas
from .caja import listar_caja, abrirCaja, cerrarCaja
from .facturas import listar_facturas, listar_facturas_detalle

def home(request):
    return listar_caja(request)

def abrir_caja(request):
    return abrirCaja(request)

def cerrar_caja(request):
    return cerrarCaja(request)

def facturas(request):
    return listar_facturas(request)

def facturas_detalle(request):
    return listar_facturas_detalle(request)

def imprimir_facturas(request):
    ids = request.GET.getlist("ids")
    facturas = Facturas.objects.filter(id__in=ids)

    return render(request, "facturas/imprimir_datos.html", {
        "facturas": facturas
    })
