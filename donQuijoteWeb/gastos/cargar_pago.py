from datetime import date
from django.shortcuts import redirect, render
from .forms import GastosForm
from .models import Gastos

def cargar_pago(request):
    hoy = date.today()
    gastos_hoy = Gastos.objects.filter(fecha=hoy)
     
    caja_total = 0.0
    caja_efectivo = 0.0
    caja_mercado = 0.0
    caja_naranja = 0.0
        
    if request.method == "POST":
        form = GastosForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('gastos:cargar_pagos') 
    else:
        form = GastosForm(request.GET or None)
       
    caja_total = 0.0
    caja_efectivo = 0.0
    caja_mercado = 0.0
    caja_naranja = 0.0  
     
    for gasto in gastos_hoy:
        caja_total += gasto.monto
        if gasto.forma_pago == "efectivo":  
            caja_efectivo += gasto.monto
        elif gasto.forma_pago == "mercado":
            caja_mercado += gasto.monto
        elif gasto.forma_pago == "naranja":
            caja_naranja += gasto.monto
        
    context = {
        'form': form,
        'gastos': gastos_hoy,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado,
        'caja_naranja': caja_naranja,
    }
    return render(request, "gastos/carga_pagos.html", context)