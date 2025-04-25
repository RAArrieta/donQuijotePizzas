from django import forms
from . import models

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = models.Proveedores
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }

class InsumosForm(forms.ModelForm):
    class Meta:
        model = models.Insumos
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "precio": forms.NumberInput(attrs={"class": "form-control"}),
            "unidad": forms.Select(attrs={"class": "form-control"}),  
            "proveedor": forms.Select(attrs={"class": "form-control"}), 
            "observacion": forms.TextInput(attrs={"class": "form-control"}),
        }

class ProductoCategoriaForm(forms.ModelForm):
    class Meta:
        model = models.ProductoCategoria
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = models.Producto
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "precio_unit": forms.TextInput(attrs={"class": "form-control"}),
            "precio_media": forms.TextInput(attrs={"class": "form-control"}),
            "precio_doc": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "precio_rec": forms.TextInput(attrs={"class": "form-control"}),
        }
        
class CantProductoForm(forms.ModelForm):
    class Meta:
        model = models.Producto
        fields = ['cantidad', 'stock']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'producto-cant', 'min': 0}),
            'stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class CantCategoriaForm(forms.ModelForm):
    class Meta:
        model = models.ProductoCategoria
        fields = ['cantidad', 'stock']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'cat-cant', 'min': 0}),
            'stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }