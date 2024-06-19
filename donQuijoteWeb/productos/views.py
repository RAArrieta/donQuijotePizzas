from django.shortcuts import render
from .models import Producto, ProductoCategoria
from . import forms, models
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView,)

def home(request):
    productos = Producto.objects.select_related('categoria').order_by('categoria__nombre').all()
    context = {
        'object_list': productos
    }
    return render(request, 'productos/index.html', context)

def categorias(request):
    categorias = ProductoCategoria.objects.all()
    return render(request, "productos/productocategoria.html", {'categorias':categorias})

class ProductosCreate(CreateView):
    model = models.Producto
    form_class = forms.ProductoForm
    success_url = reverse_lazy("productos:home")
    
class ProductoCategoriaCreate(CreateView):
    model=models.ProductoCategoria
    form_class=forms.ProductoCategoriaForm
    success_url = reverse_lazy("productos:categorias")

class ProductoUpdate(UpdateView):
    model = models.Producto
    form_class = forms.ProductoForm
    success_url = reverse_lazy("productos:home")
    
class ProductoCategoriaUpdate(UpdateView):
    model=models.ProductoCategoria
    form_class=forms.ProductoCategoriaForm
    success_url = reverse_lazy("productos:categorias")
    
class ProductoDelete(DeleteView):
    model = models.Producto
    success_url = reverse_lazy("productos:home")
    
class ProductoCategoriaDelete(DeleteView):
    model = models.ProductoCategoria
    success_url = reverse_lazy("productos:categorias")
    
class ProductoDetail(DetailView):
    model = models.Producto