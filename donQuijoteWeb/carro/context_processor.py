def importe_total_carro(request):
    total = 0.0
    if request.user.is_authenticated:
        if 'carro' in request.session: 
            for key, value in request.session["carro"].items():
                if key != "datos" and key != "empanadas" and value["precio_doc"] == "None":
                    total = float(total)+float(value["subtotal"])
                elif key == "datos" and value["precio_entrega"] != None:
                    total = float(total)+float(value["precio_entrega"])
                elif key == "empanadas":
                    total = float(total)+float(value["subtotal_emp"])

    return {"total":total}


                
    