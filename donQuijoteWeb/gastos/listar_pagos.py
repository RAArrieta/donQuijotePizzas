from django.shortcuts import render
from .models import Gastos
from core.forms import FechasPagosProvForm

def listar_pagos(request):
    gastos = Gastos.objects.all()
    
    form = FechasPagosProvForm(request.GET or None)
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        forma_pago = form.cleaned_data.get('forma_pago')
        proveedor = form.cleaned_data.get('proveedor')
        
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
    
    for gasto in gastos:
        caja_total += gasto.monto
        if gasto.forma_pago == "efectivo":  
            caja_efectivo += gasto.monto
        elif gasto.forma_pago == "mercado":
            caja_mercado += gasto.monto
        elif gasto.forma_pago == "naranja":
            caja_naranja += gasto.monto
        
    context = {
        'form': form,
        'gastos': gastos,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado,
        'caja_naranja': caja_naranja,
    }
    return render(request, "gastos/index.html", context)
