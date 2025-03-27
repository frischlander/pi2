from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Nome de usuário não pode conter caracteres especiais'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Usuário já existe'}, status=409)
        return JsonResponse({'Usuário válido': True})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('caaordserv')
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('caaordserv')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'authentication/register.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):

        username = request.POST['username']
        password = request.POST['password']
        return render(request, 'authentication/register.html')


