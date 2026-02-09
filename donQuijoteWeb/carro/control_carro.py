from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from productos.models import Producto
from pedido.models import FormaEntrega, Descuentos

from .select_productos import select_productos
from .carro import Carro
from facturas.models import Caja

def control_carro(request):
    print("def control_carro(request)")

    estado_caja = Caja.objects.all().values_list('estado_caja', flat=True)
    carro = Carro(request)
    comprobacion_pedido = carro.comprobacion_pedido()
    cargar_pedido = request.GET.get('cargar_pedido', 'false') == 'true'
    
    for estado in estado_caja:
        if not estado:
            return redirect("pedido:home")

    if cargar_pedido and comprobacion_pedido:
        return redirect("pedido:procesar_ped")

    nro_pedido = request.session.get('nro_pedido', None)
    pedido=None
    
    if nro_pedido is not None: 
        pedido= "Pedido " + str(nro_pedido)
    else:  
        if 'nro_pedido' in request.session:
            del request.session['nro_pedido']
    
    cargar_dat(request)
    carro = Carro(request)
    categorias = select_productos() 
    forma_entrega = FormaEntrega.objects.all()
    descuentos = Descuentos.objects.all()
    
    context = {
        'categorias': categorias,
        'forma_entrega': forma_entrega,
        'descuentos': descuentos,
        'pedido': pedido,
    }      
    return render(request, "carro/carro.html", context)

def cargar_dat(request):
    print("def cargar_dat(request)")
    carro=Carro(request)
    datos = {
            "estado": "",
            "hora":"",
            "pago": "",
            "forma_entrega": "",
            "descuento": "",
            "descuento_precio": 0.0,
            "precio_entrega": "",
            "envio":"",
            "nombre": "",
            "telefono": "",
            "direccion": "",
            "observacion": "",
        }
    if request.method == 'POST':        
        for field in ['estado', 'hora', 'pago', 'direccion', 'forma_entrega','descuentos', 'nombre', 'telefono', 'observacion']:
            if field in request.POST:
                datos[field]=request.POST.get(field)
                if field == 'forma_entrega':
                    entrega_id = request.POST.get("forma_entrega")
                    entrega = FormaEntrega.objects.get(id=entrega_id)
                    datos["forma_entrega"]= entrega.forma_entrega
                    datos["precio_entrega"]= entrega.precio
                    datos["envio"]= entrega.envio
                elif field == 'descuentos':
                    descuento_id = request.POST.get("descuentos")
                    descuento = Descuentos.objects.get(id=descuento_id)
                    datos["descuento"]= descuento.descuento
                    datos["descuento_precio"]= descuento.precio
                carro.agregar_datos(datos=datos) 
    carro.calcular_precio()
    return redirect("carro:carro")
