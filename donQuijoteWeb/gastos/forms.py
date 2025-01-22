from django import forms
from . import models

class RangoFechasGastosForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-contrl'}),
        label=''
    )
    fecha_fin = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-contrl'}),
        label=''
    )
    OPCIONES_FORMA_PAGO = [
        ('', 'Forma de Pago'),
        ('efectivo', 'Efectivo'),
        ('mercado', 'Mercado'),
        ('naranja', 'Naranja'),
    ]
    forma_pago = forms.ChoiceField(
        choices=OPCIONES_FORMA_PAGO,
        required=False,
        widget=forms.Select(attrs={'class': 'form-contrl'}),
        label=""
    )

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
        
