from .estadisticas_funciones import enviar_forms, cargar_estadistica

def home(request):
    return enviar_forms(request)

def cargar_datos(request):
    return cargar_estadistica(request)