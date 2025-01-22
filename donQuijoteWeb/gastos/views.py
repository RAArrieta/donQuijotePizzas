from datetime import datetime
from django.shortcuts import render
from .models import Insumos, Proveedores, Gastos
from django.views.generic import (CreateView, DeleteView, DetailView, UpdateView,)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import forms, models
from .forms import RangoFechasGastosForm

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
        
        if fecha_inicio and fecha_fin:
            gastos = gastos.filter(fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            gastos = gastos.filter(fecha__gte=fecha_inicio)
        elif fecha_fin:
            gastos = gastos.filter(fecha__lte=fecha_fin)
        
        if forma_pago:
            gastos = gastos.filter(forma_pago=forma_pago)
    
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