from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db import connection

from .models import Caja
from pedido.models import Pedido
from core.forms import PagosForm

from pedido.recuperar_pedidos import recuperar_entregados
from .facturas import cargar_fact

def abrirCaja(request):
    caja = Caja.objects.first()  
    if caja:
        caja.estado_caja = True
        caja.save() 
        
    return redirect("facturas:home")

def cerrarCaja(request):
    caja = Caja.objects.first() 

    if caja:
        cant_cobrar = Pedido.objects.filter(pago='cobrar').count()
        cant_pendientes = Pedido.objects.filter(estado='pendiente').count()        
        cant_reservados = Pedido.objects.filter(estado='reservado', pago='cobrar').count()
        cant_cancelados = Pedido.objects.filter(estado='cancelado', pago='cobrar').count()
        cant_reser_cancel = cant_reservados + cant_cancelados
        
        if cant_pendientes == 0 and (cant_cobrar == 0 or cant_reservados == cant_cobrar or cant_cancelados == cant_cobrar or cant_reser_cancel == cant_cobrar):
            cargar_fact(request)            
            Pedido.objects.exclude(estado='reservado').delete()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='pedidos'") 
                
            caja.estado_caja = False
            caja.save() 
            return redirect("facturas:home")  
        else:
            return redirect("facturas:home") 
    else:
        return redirect("core:home")


def listar_caja(request):
    pedidos = recuperar_entregados()
    pedidos_pago = None
    caja_total= 0.0
    caja_efectivo=0.0
    caja_mercado=0.0
    caja_naranja=0.0
        
    for key, value in pedidos.items():
        caja_total += value["datos"]["total"]
        if value["datos"]["pago"]=="efectivo":
            caja_efectivo += value["datos"]["total"]
        if value["datos"]["pago"]=="mercado":
            caja_mercado += value["datos"]["total"]
        if value["datos"]["pago"]=="naranja":
            caja_naranja += value["datos"]["total"]
            
    estado_caja = Caja.objects.all().values_list('estado_caja', flat=True)
    
    for estado in estado_caja:
        if not estado:
            messages.warning(request, "Caja cerrada...")
        elif caja_total == 0.0:
            messages.warning(request, "Aun no tiene pedidos entregados...")
            
    form = PagosForm(request.GET or None)

    if form.is_valid():
        forma_pago = form.cleaned_data.get('forma_pago')
    
        if forma_pago:
            pedidos_pago = {
                key: value for key, value in pedidos.items() 
                if value["datos"].get("pago") == forma_pago
            }
            pedidos = None
        
    context = {
        'form': form,
        'pedidos': pedidos,
        'pedidos_pago': pedidos_pago,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado, 
        'caja_naranja': caja_naranja
    }
    return render(request, "facturas/index.html", context)

