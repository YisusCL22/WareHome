from django.views.generic import View
from django.shortcuts import render

class HomeView(View):
    def get(self, request, *args, **kwargs):
        context={}
        return render(request, 'index.html', context)
    
class iniciarSesion(View):
    def get(self, request, *args, **kwargs):
        context={}
        return render(request, 'iniciarSesion.html', context)

class crearCuenta(View):
    def get(self, request, *args, **kwargs):
        context={}
        return render(request, 'crearCuenta.html', context)