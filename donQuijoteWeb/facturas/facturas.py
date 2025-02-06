from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Q
from datetime import datetime

from .models import Caja

from .models import Facturas, FacturaProducto
from pedido.models import Pedido

from core.forms import FechasPagosForm
from core.forms import PagosForm

from pedido.recuperar_pedidos import recuperar_entregados

def cargar_fact(request):
    pedidos = recuperar_entregados()
    
    for key, value in pedidos.items():
        envio, forma_pago, total = None, None, None
        lista_productos = list()  
        
        for k, v in value['datos'].items():
            if k == "precio_entrega":
                envio = v
            elif k == "pago":
                forma_pago = v
            elif k == "total":
                total = v  
        
        factura = Facturas(envio=envio, forma_pago=forma_pago, pago=total, )   
        
        factura.save()  

        for k, v in value.items():
            if k.isdigit(): 
                cantidad = None
                for prod_key, prod_value in v.items():
                    if prod_key == "cantidad":
                        cantidad = prod_value
                        break
                
                if cantidad is not None:
                    lista_productos.append(FacturaProducto(
                        producto_id=int(k),
                        cantidad=float(cantidad),
                        factura=factura  
                    ))
        
        FacturaProducto.objects.bulk_create(lista_productos)
        
    return redirect("core:home")

def listar_facturas(request):
    now = datetime.now()
    facturas = Facturas.objects.filter(fecha__year=now.year, fecha__month=now.month)
    productos_factura = FacturaProducto.objects.all()
    
    form = FechasPagosForm(request.GET or None)
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        forma_pago = form.cleaned_data.get('forma_pago')
        
        if fecha_inicio and fecha_fin:
            facturas = Facturas.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        
        if forma_pago:
            facturas = facturas.filter(forma_pago=forma_pago)
  
    caja_total = 0.0
    caja_efectivo = 0.0
    caja_mercado = 0.0
    caja_naranja = 0.0
       
    facturas_aggregates = facturas.aggregate(
        total=Sum('pago'),
        efectivo=Sum('pago', filter=Q(forma_pago="efectivo")),
        mercado=Sum('pago', filter=Q(forma_pago="mercado")),
        naranja=Sum('pago', filter=Q(forma_pago="naranja"))
    )

    caja_total = (facturas_aggregates['total'] or 0) 
    caja_efectivo = (facturas_aggregates['efectivo'] or 0) 
    caja_mercado = (facturas_aggregates['mercado'] or 0)
    caja_naranja = (facturas_aggregates['naranja'] or 0) 
 
    context = {
        'form': form,
        'facturas': facturas,
        'productos_factura': productos_factura,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado,
        'caja_naranja': caja_naranja,
    }
    
    return render(request, "facturas/facturas.html", context)    