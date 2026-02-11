from django.shortcuts import render, redirect
from django.db.models import Sum, Q
from django.utils import timezone

from .models import Caja
from .models import Facturas, FacturaProducto
from core.forms import FechasPagosForm
from pedido.recuperar_pedidos import recuperar_pedidos

def cargar_fact(request):   
    datos_pedidos = recuperar_pedidos('entregado')
    pedidos = datos_pedidos.get("pedidos", {})  
    pedidos_reservados = datos_pedidos.get("pedidos_reservados", {}) 
    caja = Caja.objects.first()
    turno = caja.turno if caja else None
    
    print("*************************")
    print(pedidos)
    print("*************************")

    for key, value in pedidos.items():
        cargar_factura(key, value, turno)
        
    for key, value in pedidos_reservados.items():
        cargar_factura(key, value, turno)
                    
    return redirect("core:home")

def cargar_factura(key, value, turno):
    descuento, direccion, nombre, envio, forma_pago, telefono, total = None, None, None, None, None, None, None
    lista_productos = list()  
    
    pedido = key
    
    for k, v in value['datos'].items():
        if k == "forma_entrega" and v == "Retira":
            envio = False
        elif k == "forma_entrega" and v != "Retira":
            envio = True
        elif k == "pago":
            forma_pago = v
        elif k == "telefono":
            telefono = v
        elif k == "direccion":
            direccion = v
        elif k == "nombre":
            nombre = v
        elif k == "descuento":
            descuento = v
        elif k == "total":
            total = v  
    
    factura = Facturas(envio=envio, forma_pago=forma_pago, pago=total, turno=turno, telefono=telefono, direccion=direccion, nombre=nombre, descuento=descuento, pedido=pedido )   
    
    factura.save()  

    for k, v in value.items():
        subtotal, cantidad = None, None
        for prod_key, prod_value in v.items():
            if prod_key == "cantidad":
                cantidad = prod_value
            if prod_key == "subtotal" or prod_key == "subtotal_emp":
                subtotal = prod_value
        
        if cantidad is not None:
            if k == 'empanadas':
                lista_productos.append(FacturaProducto(
                    empanadas=str(k),
                    cantidad=float(cantidad),
                    subtotal = float(subtotal),
                    factura=factura  
                ))
            else:
                lista_productos.append(FacturaProducto(
                    producto_id=int(k),
                    cantidad=float(cantidad),
                    subtotal = float(subtotal),
                    factura=factura  
                ))
    
    FacturaProducto.objects.bulk_create(lista_productos)
        

def listar_facturas(request, key):
    print(f"key: {key}")
    today = timezone.now().date()
    facturas = Facturas.objects.filter(fecha__year=today.year, fecha__month=today.month)
    
    form = FechasPagosForm(request.GET or None)
    
    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        forma_pago = form.cleaned_data.get('forma_pago')
        turno = form.cleaned_data.get('turno')
        
        if fecha_inicio and fecha_fin:
            facturas = Facturas.objects.filter(fecha__range=[fecha_inicio, fecha_fin])           
        if forma_pago:
            facturas = facturas.filter(forma_pago=forma_pago)
        if turno:
            facturas = facturas.filter(turno=turno)
       
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
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado,
        'caja_naranja': caja_naranja,
    }
    
    if key == "detalle":
        productos_factura = FacturaProducto.objects.filter(factura__in=facturas)
        context["productos_factura"] = productos_factura
        return render(request, "facturas/facturas_detalle.html", context)
    
    return render(request, "facturas/facturas.html", context) 