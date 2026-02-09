from django import forms
from . import models

class FormaEntregaForm(forms.ModelForm):
    class Meta:
        model = models.FormaEntrega
        fields = ['forma_entrega', 'precio']
        widgets = {
            "forma_entrega": forms.TextInput(attrs={"class": "form-control"}),
            'precio': forms.NumberInput(attrs={'step': 'any', "class": "form-control"})
        }
        
class DescuentosForm(forms.ModelForm):
    class Meta:
        model = models.Descuentos
        fields = ['descuento', 'precio']
        widgets = {
            "descuento": forms.TextInput(attrs={"class": "form-control"}),
            'precio': forms.NumberInput(attrs={'step': 'any', "class": "form-control"})
        }