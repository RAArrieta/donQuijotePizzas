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
            "unidad": forms.Select(attrs={"class": "form-control"}),  # Cambiado a Select
            "proveedor": forms.Select(attrs={"class": "form-control"}),  # Esto es correcto
        }