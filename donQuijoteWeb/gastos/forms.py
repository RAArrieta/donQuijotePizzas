from django import forms
from . import models

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
        

            
  
           
