from django.shortcuts import render

def home(request):
    saludo = "Hooooola Gastos"
        
    context = {
        'saludo': saludo,
    }
    return render(request, "gastos/index.html", context)