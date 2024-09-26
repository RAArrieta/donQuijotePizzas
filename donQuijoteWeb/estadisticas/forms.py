from django import forms
import datetime

MESES = [
    (0, "Todos los meses"),  
    (1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"),
    (5, "Mayo"), (6, "Junio"), (7, "Julio"), (8, "Agosto"),
    (9, "Septiembre"), (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre")
]

class MesAnoForm(forms.Form):
    mes = forms.ChoiceField(choices=MESES, label='Mes', widget=forms.Select(attrs={'class': 'select'}))
    ano = forms.IntegerField(
        label='Año',
        widget=forms.Select(choices=[(year, year) for year in range(2024, 2044)], attrs={'class': 'select'})
    )

    def __init__(self, *args, **kwargs):
        super(MesAnoForm, self).__init__(*args, **kwargs)
        now = datetime.datetime.now()
        self.fields['mes'].initial = now.month
        self.fields['ano'].initial = now.year


