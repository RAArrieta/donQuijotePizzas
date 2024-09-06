from datetime import datetime
from django.shortcuts import render, redirect
from pedido.recuperar_pedidos import recuperar_entregados
from django.contrib import messages
from .models import Caja, Facturas
from pedido.models import Pedido
from django.db import connection
from datetime import datetime
from .forms import RangoFechasForm

def home(request):
    pedidos = recuperar_entregados()
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
        
    context = {
        'pedidos': pedidos,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado, 
        'caja_naranja': caja_naranja
    }
    return render(request, "facturas/index.html", context)

def abrir_caja(request):
    caja = Caja.objects.first()  
    if caja:
        caja.estado_caja = True
        caja.save() 
    return redirect("facturas:home")

def cerrar_caja(request):
    caja = Caja.objects.first()  
    if caja:
        cant_pendientes = Pedido.objects.filter(estado='pendiente').count()
        cant_cobrar = Pedido.objects.filter(pago='cobrar').count()
        if cant_pendientes == 0 and cant_cobrar == 0:
            cargar_facturas()            
            Pedido.objects.all().delete()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='pedidos'") 
                
            caja.estado_caja = False
            caja.save() 
            return redirect("facturas:home")  
        elif cant_pendientes != 0:
            messages.error(request, "Tienes pedidos pendientes, debes marcarlos como entregado o cancelarlos...")
            return redirect("facturas:home") 
        elif cant_cobrar != 0:
            messages.error(request, "Tienes pedidos por cobrar...")
            return redirect("facturas:home")
    else:
        messages.error(request, "No hay una instancia de Caja disponible.")
        return redirect("core:home")

def cargar_facturas():
    pedidos = recuperar_entregados()
    
    for key, value in pedidos.items():
        forma_pago = value["datos"]["pago"]
        total = value["datos"]["total"]
        
        factura = Facturas(
            forma_pago=forma_pago,
            pago=total,
        )

        
        factura.save() 

    return redirect("core:home")

def facturas(request):
    now = datetime.now()
    facturas = Facturas.objects.filter(fecha__year=now.year, fecha__month=now.month)
       
    caja_total= 0.0
    caja_efectivo=0.0
    caja_mercado=0.0
    caja_naranja=0.0
        
    for factura in facturas:
        caja_total += factura.pago
        if factura.forma_pago == "efectivo":  
            caja_efectivo += factura.pago
        elif factura.forma_pago == "mercado":
            caja_mercado += factura.pago
        elif factura.forma_pago == "naranja":
            caja_naranja += factura.pago
    
    form = RangoFechasForm(request.GET or None)
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        facturas = Facturas.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        
        caja_total= 0.0
        caja_efectivo=0.0
        caja_mercado=0.0
        caja_naranja=0.0
        
        for factura in facturas:
            caja_total += factura.pago
            if factura.forma_pago == "efectivo":  
                caja_efectivo += factura.pago
            elif factura.forma_pago == "mercado":
                caja_mercado += factura.pago
            elif factura.forma_pago == "naranja":
                caja_naranja += factura.pago
    
    context = {
        'form': form,
        'facturas': facturas,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado, 
        'caja_naranja': caja_naranja,
    }
    
    return render(request, "facturas/facturas.html", context)
