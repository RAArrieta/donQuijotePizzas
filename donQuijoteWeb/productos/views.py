from django.shortcuts import render
from .models import Producto, ProductoCategoria
from pedido.models import FormaEntrega
from . import forms, models
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, UpdateView,)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    productos = Producto.objects.select_related('categoria').order_by('categoria__nombre').all()
    categorias = ProductoCategoria.objects.all()
    forma_entrega = FormaEntrega.objects.all()
    
    context = {
        'object_list': productos,
        'categorias': categorias,
        'forma_entrega': forma_entrega
    }
    return render(request, 'productos/index.html', context)

@login_required
def categorias(request):
    categorias = ProductoCategoria.objects.all()
    return render(request, "productos/productocategoria.html", {'categorias':categorias})

class ProductosCreate(LoginRequiredMixin, CreateView):
    model = models.Producto
    form_class = forms.ProductoForm
    success_url = reverse_lazy("productos:home")
    
class ProductoCategoriaCreate(LoginRequiredMixin, CreateView):
    model=models.ProductoCategoria
    form_class=forms.ProductoCategoriaForm
    success_url = reverse_lazy("productos:categorias")

class ProductoUpdate(LoginRequiredMixin, UpdateView):
    model = models.Producto
    form_class = forms.ProductoForm
    success_url = reverse_lazy("productos:home")
    
class ProductoCategoriaUpdate(LoginRequiredMixin, UpdateView):
    model=models.ProductoCategoria
    form_class=forms.ProductoCategoriaForm
    success_url = reverse_lazy("productos:categorias")
    
class ProductoDelete(LoginRequiredMixin, DeleteView):
    model = models.Producto
    success_url = reverse_lazy("productos:home")
    
class ProductoCategoriaDelete(LoginRequiredMixin, DeleteView):
    model = models.ProductoCategoria
    success_url = reverse_lazy("productos:categorias")
    
class ProductoDetail(LoginRequiredMixin, DetailView):
    model = models.Producto

@login_required
def lista_wa(request):
    productos = Producto.objects.select_related('categoria').order_by('categoria__nombre').all()
    context = {
        'object_list': productos
    }
    return render(request, 'productos/lista_wa.html', context)