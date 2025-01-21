from django.shortcuts import render
from .models import Insumos, Proveedores
from django.views.generic import (CreateView, DeleteView, DetailView, UpdateView,)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import forms, models

def home(request):
    saludo = "Hooooola Gastos"
        
    context = {
        'saludo': saludo,
    }
    return render(request, "gastos/index.html", context)

class InsumosCreate(LoginRequiredMixin, CreateView):
    model = models.Insumos
    form_class = forms.InsumosForm
    success_url = reverse_lazy("gastos:home")