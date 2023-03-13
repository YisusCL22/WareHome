
from django.http import HttpResponse
import datetime
from django.template import *
def saludo(request):

    return HttpResponse("Bienvenidos a la Pagina Principal")

def get_fecha(request):
    fecha=datetime.datetime.now()
    textofecha="Fecha y Hora: %s." %fecha

    return HttpResponse(textofecha)
    

