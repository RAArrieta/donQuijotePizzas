from django import forms
from . import models

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
        }