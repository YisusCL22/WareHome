from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def home(request):
    template = loader.get_template('Home.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template('Login.html')
    context = {}
    return HttpResponse(template.render(context, request))