def importe_total_carro(request):
    total = 350
    if request.user.is_authenticated:
        if 'carro' in request.session: 
            for key, value in request.session["carro"].items():
                total = total + (float(value["precio"])*value["cantidad"])
    return {"importe_total_carro":total}