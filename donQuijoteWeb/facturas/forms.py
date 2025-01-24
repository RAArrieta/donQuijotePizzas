from django import forms

class RangoFechasForm(forms.Form):
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
    


    