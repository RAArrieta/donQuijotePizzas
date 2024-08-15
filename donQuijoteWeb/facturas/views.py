from django.shortcuts import render
from pedido.recuperar_pedidos import recuperar_entregados

def home(request):
    pedidos = recuperar_entregados()
    caja_total= 0.0
    caja_efectivo=0.0
    caja_mercado=0.0
    caja_naranja=0.0

    for key, value in pedidos.items():
        caja_total += value["datos"]["total"]
        if value["datos"]["pago"]=="efectivo":
            caja_efectivo += value["datos"]["total"]
        if value["datos"]["pago"]=="mercado":
            caja_mercado += value["datos"]["total"]
        if value["datos"]["pago"]=="naranja":
            caja_naranja += value["datos"]["total"]
        
    context = {
        'pedidos': pedidos,
        'caja_total': caja_total,
        'caja_efectivo': caja_efectivo,
        'caja_mercado': caja_mercado, 
        'caja_naranja': caja_naranja
    }
    return render(request, "facturas/index.html", context)
