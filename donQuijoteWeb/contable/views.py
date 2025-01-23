from datetime import datetime
from django.shortcuts import render

from gastos.forms import RangoFechasGastosForm
from gastos.models import Gastos
from facturas.models import Facturas
from django.db.models import Sum, Value, F, Q
from datetime import date
from itertools import chain

def home(request):
    hoy = date.today()
    inicio_mes = date(hoy.year, hoy.month, 1)
    
    gastos_xdia = Gastos.objects.filter(fecha__gte=inicio_mes).values('fecha').annotate(total_gastado=Sum('monto'), nombre=Value('PAGOS')).order_by('fecha')
    facturas_xdia = Facturas.objects.filter(fecha__gte=inicio_mes).values('fecha').annotate(total_gastado=Sum('pago'), nombre=Value('FACTURACION')).order_by('fecha')
    
    gastos_facturas_xdia = sorted(
        chain(gastos_xdia, facturas_xdia),
        key=lambda x: x['fecha'],
        reverse=True
    )
    
    
    
    
    
    
    
    
    
    
       
    # for factura in facturas:
    #     caja_total += factura.pago
    #     if factura.forma_pago == "efectivo":  
    #         caja_efectivo += factura.pago
    #     elif factura.forma_pago == "mercado":
    #         caja_mercado += factura.pago
    #     elif factura.forma_pago == "naranja":
    #         caja_naranja += factura.pago
            
    # for gasto in gastos:
    #     caja_total -= gasto.monto
    #     if gasto.forma_pago == "efectivo":  
    #         caja_efectivo -= gasto.monto
    #     elif gasto.forma_pago == "mercado":
    #         caja_mercado -= gasto.monto
    #     elif gasto.forma_pago == "naranja":
    #         caja_naranja -= gasto.monto


    caja_total = 0.0
    caja_efectivo = 0.0
    caja_mercado = 0.0
    caja_naranja = 0.0
    
    facturas_aggregates = Facturas.objects.aggregate(
        total=Sum('pago'),
        efectivo=Sum('pago', filter=Q(forma_pago="efectivo")),
        mercado=Sum('pago', filter=Q(forma_pago="mercado")),
        naranja=Sum('pago', filter=Q(forma_pago="naranja"))
    )

    gastos_aggregates = Gastos.objects.aggregate(
        total=Sum('monto'),
        efectivo=Sum('monto', filter=Q(forma_pago="efectivo")),
        mercado=Sum('monto', filter=Q(forma_pago="mercado")),
        naranja=Sum('monto', filter=Q(forma_pago="naranja"))
    )

    caja_total = (facturas_aggregates['total'] or 0) - (gastos_aggregates['total'] or 0)
    caja_efectivo = (facturas_aggregates['efectivo'] or 0) - (gastos_aggregates['efectivo'] or 0)
    caja_mercado = (facturas_aggregates['mercado'] or 0) - (gastos_aggregates['mercado'] or 0)
    caja_naranja = (facturas_aggregates['naranja'] or 0) - (gastos_aggregates['naranja'] or 0)
        
    context = {
        'gastos_facturas': gastos_facturas_xdia,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado,
        'caja_naranja': caja_naranja,
    }
    return render(request, "contable/index.html", context)