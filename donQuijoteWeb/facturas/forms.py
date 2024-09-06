from django import forms

class RangoFechasForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-contrl'}),
        label=''
    )
    fecha_fin = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-contrl'}),
        label=''
    )
