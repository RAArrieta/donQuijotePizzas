from django import forms

class RangoFechasForm(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))