from datetime import date, datetime
from django.shortcuts import redirect, render, get_object_or_404
from .models import Insumos, Proveedores, Gastos
from django.views.generic import (CreateView, DeleteView, DetailView, UpdateView,)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import forms, models
from .forms import RangoFechasGastosForm, GastosForm

def home(request):
    gastos = Gastos.objects.all()
    now = datetime.now()
    
    caja_total = 0.0
    caja_efectivo = 0.0
    caja_mercado = 0.0
    caja_naranja = 0.0
    
    form = RangoFechasGastosForm(request.GET or None)
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        forma_pago = form.cleaned_data.get('forma_pago')
        insumo = form.cleaned_data.get('insumo')
        proveedor = form.cleaned_data.get('proveedor')
        
        if fecha_inicio and fecha_fin:
            gastos = gastos.filter(fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            gastos = gastos.filter(fecha__gte=fecha_inicio)
        elif fecha_fin:
            gastos = gastos.filter(fecha__lte=fecha_fin)
        
        if forma_pago:
            gastos = gastos.filter(forma_pago=forma_pago)
        
        if insumo:
            gastos = gastos.filter(insumo=insumo)
        
        if proveedor:
            gastos = gastos.filter(insumo__proveedor=proveedor)
    
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

def listar_insumos(request):
    insumos = Insumos.objects.select_related('proveedor').order_by('proveedor__nombre')
    proveedores = Proveedores.objects.all()
    
    context = {
        'object_list': insumos,
        'proveedores': proveedores,
    }
    return render(request, "gastos/listar_insumos.html", context)

def listar_proveedores(request):
    proveedores = Proveedores.objects.all()
    
    context = {
        'proveedores': proveedores,
    }
    return render(request, "gastos/listar_proveedores.html", context)
   

class InsumosCreate(LoginRequiredMixin, CreateView):
    model = models.Insumos
    form_class = forms.InsumosForm
    success_url = reverse_lazy("gastos:home")
    
class ProveedoresCreate(LoginRequiredMixin, CreateView):
    model = models.Proveedores
    form_class = forms.ProveedoresForm
    success_url = reverse_lazy("gastos:home")
    
class InsumosUpdate(LoginRequiredMixin, UpdateView):
    model = models.Insumos
    form_class = forms.InsumosForm
    success_url = reverse_lazy("gastos:home")
    
class ProveedoresUpdate(LoginRequiredMixin, UpdateView):
    model = models.Proveedores
    form_class = forms.ProveedoresForm
    success_url = reverse_lazy("gastos:home")
    
def cargar_pagos(request):
    hoy = date.today()
    gastos_hoy = Gastos.objects.filter(fecha=hoy)
     
    caja_total = 0.0
    caja_efectivo = 0.0
    caja_mercado = 0.0
    caja_naranja = 0.0
    

    
    if request.method == "POST":
        # Procesar el formulario enviado
        form = GastosForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos del formulario en la base de datos
            return redirect('gastos:cargar_pagos')  # Redirige a la misma vista para evitar reenvíos
    else:
        # Crear un formulario vacío para mostrar en el template
        form = GastosForm(request.GET or None)
       
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

def eliminar_pago(request, gasto_id):
        # Obtiene el gasto por ID o muestra un error 404 si no existe
    gasto = get_object_or_404(Gastos, id=gasto_id)
    
    # Elimina el gasto
    gasto.delete()
    


    return redirect('gastos:cargar_pagos')