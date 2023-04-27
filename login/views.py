from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import LoginForm
from django.views.generic import FormView, RedirectView

from django.contrib.auth import login, logout
import requests
from django.http import HttpResponseRedirect

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from django.contrib import auth
from django.views import View
from django.http import HttpResponse
from django.contrib import messages


class LoginView(FormView):
    template_name = 'log/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        response = requests.post('http://127.0.0.1:8000/api/log/', json={'username': username, 'password': password})
        if response.status_code == 200:
            try:
                u = response.json()
                token = u['token']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(self.request, user)
                    response = HttpResponseRedirect(self.success_url)
                    response.set_cookie('access', value=token)
                    messages.success(self.request, 'Bienvenido')
                    return response
                else:
                    messages.error(self.request, 'No se pudo autenticar al usuario')
            except ValueError:
                messages.error(self.request, 'Error en la respuesta de la API de login')
        else:
            messages.error(self.request, 'Credenciales de inicio de sesión incorrectas')
        return redirect('Login:login')





class LogoutView(View):
  
    def get(self, request):
        token = request.COOKIES.get('access')
        if not token:
            messages.error(self.request, 'No se ha proporcionado un token de autenticación.')
            return redirect('accounts:home')
        
        headers = {'Authorization': f'Token {token}'}  # corrected the typo here
        response = requests.get('http://127.0.0.1:8000/api/out/', headers=headers)
        if response.status_code == 200:
            auth.logout(request)
            response = redirect('home')
            response.delete_cookie('access')
            response.delete_cookie('csrftoken')

            messages.success(self.request, 'Se ha cerrado sesión correctamente.')
            return response

        messages.error(self.request, 'No se pudo cerrar sesión. Por favor, intenta de nuevo más tarde.')
        return redirect('accounts:home')












