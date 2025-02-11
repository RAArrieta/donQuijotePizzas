from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, ProductoCategoria, Insumos, Proveedores, ProductoInsumos
from pedido.models import FormaEntrega
from . import forms, models
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, UpdateView,)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from .precio_recomendado import precio_recomendado

@login_required
def home(request):
    productos = Producto.objects.select_related('categoria').order_by('categoria__nombre').all()
    categorias = ProductoCategoria.objects.all()
    forma_entrega = FormaEntrega.objects.all()
    precio_recomendado()
    
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
    
@login_required
def lista_wa(request):
    productos = Producto.objects.select_related('categoria').order_by('categoria__nombre').all()
    context = {
        'object_list': productos
    }
    return render(request, 'productos/lista_wa.html', context)

def listar_insumos(request):
    insumos = Insumos.objects.select_related('proveedor').order_by('proveedor__nombre')
    proveedores = Proveedores.objects.all()
    
    context = {
        'object_list': insumos,
        'proveedores': proveedores,
    }
    return render(request, "productos/listar_insumos.html", context)

def listar_proveedores(request):
    proveedores = Proveedores.objects.all()
    
    context = {
        'proveedores': proveedores,
    }
    return render(request, "productos/listar_proveedores.html", context)
   

class InsumosCreate(LoginRequiredMixin, CreateView):
    model = models.Insumos
    form_class = forms.InsumosForm
    success_url = reverse_lazy("productos:listar_insumos")
    
class ProveedoresCreate(LoginRequiredMixin, CreateView):
    model = models.Proveedores
    form_class = forms.ProveedoresForm
    success_url = reverse_lazy("productos:listar_proveedores")
    
class InsumosUpdate(LoginRequiredMixin, UpdateView):
    model = models.Insumos
    form_class = forms.InsumosForm
    success_url = reverse_lazy("productos:listar_insumos")
    
class ProveedoresUpdate(LoginRequiredMixin, UpdateView):
    model = models.Proveedores
    form_class = forms.ProveedoresForm
    success_url = reverse_lazy("productos:listar_proveedores")

def agregar_insumos_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    insumos = Insumos.objects.all()
    estado_choices = ProductoInsumos.ESTADO_CHOICES
    producto_insumos = ProductoInsumos.objects.filter(producto=producto)  # Traer insumos ya asociados

    if request.method == "POST":
        insumo_ids = request.POST.getlist('insumo')
        cantidades = request.POST.getlist('cantidad')
        unidades = request.POST.getlist('unidad')
        eliminar_ids = request.POST.getlist('eliminar_insumo')  # Insumos a eliminar

        # Eliminar insumos seleccionados
        if eliminar_ids:
            ProductoInsumos.objects.filter(id__in=eliminar_ids, producto=producto).delete()
            return redirect('productos:agregar_insumos_producto')

        for insumo_id, cantidad, unidad in zip(insumo_ids, cantidades, unidades):
            if insumo_id and cantidad:
                insumo = get_object_or_404(Insumos, id=insumo_id)

                producto_insumo, created = ProductoInsumos.objects.get_or_create(
                    producto=producto,
                    insumo=insumo,
                    defaults={'cantidad': float(cantidad), 'unidad': unidad}
                )
                
                if not created:
                    producto_insumo.cantidad = float(cantidad)
                    producto_insumo.unidad = unidad
                    producto_insumo.save()

        return redirect('productos:home')  

      
    for insumo in producto_insumos:
        insumo.cantidad = str(insumo.cantidad).replace(",", ".")


    context = {
        'producto': producto, 
        'insumos': insumos,
        'producto_insumos': producto_insumos,  
        "ESTADO_CHOICES": estado_choices
    }
    return render(request, 'productos/agregar_insumos.html', context)

def eliminar_insumo(request, insumo_id):
    insumo = get_object_or_404(ProductoInsumos, id=insumo_id)
    producto_id = insumo.producto.id  # Obtener el ID del producto para redireccionar
    insumo.delete()
    return redirect('productos:agregar_insumos_producto', producto_id=producto_id)




