from django.shortcuts import redirect, render, get_object_or_404
from .models import Gastos


from .listar_pagos import listar_pagos
from .cargar_pago import cargar_pago

def home(request):
    return listar_pagos(request)
    
def cargar_pagos(request):
    return cargar_pago(request)

def eliminar_pago(request, gasto_id):
    gasto = get_object_or_404(Gastos, id=gasto_id)
    gasto.delete()
    return redirect('gastos:cargar_pagos')