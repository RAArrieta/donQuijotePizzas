from django.contrib.auth.forms import AuthenticationForm
from django import forms
from gastos.models import Proveedores

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = "Usuario"
        self.fields['password'].label = "Contraseña"
        
class FechasForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=''
    )
    fecha_fin = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=''
    )

class FechasPagosForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label=''
    )
    fecha_fin = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
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
    
class FechasPagosProvForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label=''
    )
    fecha_fin = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
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
    # insumo = forms.ModelChoiceField(
    #     queryset=Insumos.objects.all(),
    #     required=False,
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     label="",
    #     empty_label="Insumos" 
    # )