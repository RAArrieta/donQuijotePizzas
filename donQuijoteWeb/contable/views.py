from datetime import datetime
from django.shortcuts import render

from gastos.forms import RangoFechasGastosForm
from gastos.models import Gastos
from facturas.models import Facturas
from django.db.models import Sum, Value
from itertools import chain

def home(request):
    gastos = Gastos.objects.all()
    facturas = Facturas.objects.all()
    gastos_xdia = Gastos.objects.values('fecha').annotate(total_gastado=Sum('monto'), nombre=Value('PAGOS')).order_by('fecha')
    facturas_xdia = Facturas.objects.values('fecha').annotate(total_gastado=Sum('pago'), nombre=Value('FACTURACION')).order_by('fecha')
    
    gastos_facturas_xdia = sorted(
        chain(gastos_xdia, facturas_xdia),
        key=lambda x: x['fecha'],
        reverse=True
    )
    
    caja_total = 0.0
    caja_efectivo = 0.0
    caja_mercado = 0.0
    caja_naranja = 0.0
       
    for factura in facturas:
        caja_total += factura.pago
        if factura.forma_pago == "efectivo":  
            caja_efectivo += factura.pago
        elif factura.forma_pago == "mercado":
            caja_mercado += factura.pago
        elif factura.forma_pago == "naranja":
            caja_naranja += factura.pago
            
    for gasto in gastos:
        caja_total -= gasto.monto
        if gasto.forma_pago == "efectivo":  
            caja_efectivo -= gasto.monto
        elif gasto.forma_pago == "mercado":
            caja_mercado -= gasto.monto
        elif gasto.forma_pago == "naranja":
            caja_naranja -= gasto.monto
        
    context = {
        'gastos_facturas': gastos_facturas_xdia,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado,
        'caja_naranja': caja_naranja,
    }
    return render(request, "contable/index.html", context)