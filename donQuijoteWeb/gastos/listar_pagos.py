from django.shortcuts import render
from django.db.models import Sum, Q
from datetime import datetime
from .models import Gastos
from core.forms import FechasPagosProvForm


def listar_pagos(request):
    now = datetime.now()
    gastos = Gastos.objects.filter(fecha__year=now.year, fecha__month=now.month)
       
    form = FechasPagosProvForm(request.GET or None)  
    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        forma_pago = form.cleaned_data.get('forma_pago')
        proveedor = form.cleaned_data.get('proveedor')
        gastos = Gastos.objects.all()
        
        if fecha_inicio and fecha_fin:
            gastos = gastos.filter(fecha__range=[fecha_inicio, fecha_fin])
               
        if forma_pago:
            gastos = gastos.filter(forma_pago=forma_pago)
             
        if proveedor:
            gastos = gastos.filter(proveedor=proveedor)
    
    caja_total = 0.0
    caja_efectivo = 0.0
    caja_mercado = 0.0
    caja_naranja = 0.0
    
    gastos_aggregates = gastos.aggregate(
        total=Sum('monto'),
        efectivo=Sum('monto', filter=Q(forma_pago="efectivo")),
        mercado=Sum('monto', filter=Q(forma_pago="mercado")),
        naranja=Sum('monto', filter=Q(forma_pago="naranja"))
    )

    caja_total = (gastos_aggregates['total'] or 0) 
    caja_efectivo = (gastos_aggregates['efectivo'] or 0) 
    caja_mercado = (gastos_aggregates['mercado'] or 0)
    caja_naranja = (gastos_aggregates['naranja'] or 0) 
        
    context = {
        'form': form,
        'gastos': gastos,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado,
        'caja_naranja': caja_naranja,
    }
    return render(request, "gastos/index.html", context)
