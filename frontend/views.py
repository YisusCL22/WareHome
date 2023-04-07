from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings 
from django.contrib import messages 
from registration.models import Profile

from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def home(request):
    template = loader.get_template('Home.html')
    context = {}
    return HttpResponse(template.render(context, request))

    
class CustomLoginView(FormView):
    form_class = LoginForm
    template_name = 'Login.html'
    success_url = reverse_lazy('check_profile')

    def form_valid(self, form):
        usuario = form.cleaned_data.get('user')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=usuario, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Correo electrónico o contraseña inválidos')
            return self.form_invalid(form)
        
@login_required
def pre_check_profile(request):
    return redirect('check_profile')


@login_required
def check_profile(request):  
    try:
        profile = Profile.objects.filter(user_id=request.user.id).get()    
    except:
        messages.add_message(request, messages.INFO, 'Hubo un error con su usuario, por favor contactese con los administradores')              
        return redirect('Login')
    if profile.group_id == 1: 
        return redirect('admin_main')
    #elif profile.group_id == 2: 
        #return redirect('cuenta')
    else:
        return redirect('Home')
    