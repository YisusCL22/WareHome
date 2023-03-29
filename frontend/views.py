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


def LoginView(request):
    form_class = LoginForm
    template_name = 'Login.html'
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'Login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        success_url = reverse_lazy('check_login')
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,username=email,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hola {email.title()}, Hola')
                return redirect('home')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Email o Contraseña inválida')
        return render(request,'Login.html',{'form': form})
    
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
        return HttpResponse('Usted se ha autentificado')
        #return redirect('admin_main')
    else:
        return redirect('logout')