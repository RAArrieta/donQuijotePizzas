from django.shortcuts import render
from core.forms import FechasForm

from gastos.models import Gastos
from facturas.models import Facturas
from django.db.models import Sum, Value, Q

from datetime import date
from itertools import chain


def tesoreria(request):
    hoy = date.today()
    inicio_mes = date(hoy.year, hoy.month, 1)  

    gastos = Gastos.objects.all()
    facturas = Facturas.objects.all()

    form = FechasForm(request.GET or None)

    gastos_xdia = Gastos.objects.none()
    facturas_xdia = Facturas.objects.none()

    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            facturas = facturas.filter(fecha__range=[fecha_inicio, fecha_fin])
            gastos = gastos.filter(fecha__range=[fecha_inicio, fecha_fin])

            gastos_xdia = gastos.values('fecha').annotate(total_gastado=Sum('monto'), nombre=Value('Pagos')).order_by('fecha')
            facturas_xdia = facturas.values('fecha').annotate(total_gastado=Sum('pago'), nombre=Value('Facturación')).order_by('fecha')

    else:
        gastos_xdia = gastos.filter(fecha__gte=inicio_mes).values('fecha').annotate(total_gastado=Sum('monto'), nombre=Value('Pagos')).order_by('fecha')
        facturas_xdia = facturas.filter(fecha__gte=inicio_mes).values('fecha').annotate(total_gastado=Sum('pago'), nombre=Value('Facturación')).order_by('fecha')

    gastos_facturas_xdia = sorted(
        chain(gastos_xdia, facturas_xdia),
        key=lambda x: x['fecha'],
    )
    
    caja_total = 0.0
    caja_efectivo = 0.0
    caja_mercado = 0.0
    caja_naranja = 0.0
       
    facturas_aggregates = facturas.aggregate(
        total=Sum('pago'),
        efectivo=Sum('pago', filter=Q(forma_pago="efectivo")),
        mercado=Sum('pago', filter=Q(forma_pago="mercado")),
        naranja=Sum('pago', filter=Q(forma_pago="naranja"))
    )

    gastos_aggregates = gastos.aggregate(
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
        'form': form,
        'gastos_facturas': gastos_facturas_xdia,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado,
        'caja_naranja': caja_naranja,
    }
    return render(request, "contable/index.html", context)