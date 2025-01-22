from django import forms
from . import models
from .models import Insumos, Proveedores

class RangoFechasGastosForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=''
    )
    fecha_fin = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
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
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=""
    )
    proveedor = forms.ModelChoiceField(
        queryset=Proveedores.objects.filter(estado=True),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="",
        empty_label="Proveedores"
    )
   
    insumo = forms.ModelChoiceField(
        queryset=Insumos.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="",
        empty_label="Insumos" 
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

class GastosForm(forms.ModelForm):
    class Meta:
        model = models.Gastos
        exclude = ["fecha"]
        widgets = {
            "insumo": forms.Select(attrs={"class": "form-control"}),  
            "cantidad": forms.NumberInput(attrs={"class": "form-control"}),
            "monto": forms.NumberInput(attrs={"class": "form-control"}),
            "forma_pago": forms.Select(attrs={"class": "form-control"}),
            
        }  
        

            
  
           
