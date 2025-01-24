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
        }

class GastosForm(forms.ModelForm):
    class Meta:
        model = models.Gastos
        exclude = ["fecha"]
        widgets = {
            "proveedor": forms.Select(attrs={"class": "form-control"}),  
            "cantidad": forms.NumberInput(attrs={"class": "form-control"}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
            "forma_pago": forms.Select(attrs={"class": "form-control"}),
            
        }  
        

            
  
           
