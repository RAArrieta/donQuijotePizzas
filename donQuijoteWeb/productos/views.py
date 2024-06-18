from django.shortcuts import render
from .models import Producto
from . import forms, models
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView,)

def home(request):
    productos = Producto.objects.select_related('categoria').order_by('categoria__nombre').all()
    context = {
        'object_list': productos
    }
    return render(request, 'productos/index.html', context)

class ProductosCreate(CreateView):
    model = models.Producto
    form_class = forms.ProductoForm
    success_url = reverse_lazy("productos:home")

class ProductoUpdate(UpdateView):
    model = models.Producto
    form_class = forms.ProductoForm
    success_url = reverse_lazy("productos:home")
    
class ProductoDelete(DeleteView):
    model = models.Producto
    success_url = reverse_lazy("productos:home")
    
class ProductoDetail(DetailView):
    model = models.Producto