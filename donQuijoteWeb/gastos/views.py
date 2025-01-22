from django.shortcuts import render
from .models import Insumos, Proveedores, Gastos
from django.views.generic import (CreateView, DeleteView, DetailView, UpdateView,)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import forms, models

def home(request):
    gastos = Gastos.objects.all()
        
    context = {
        'gastos': gastos,
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