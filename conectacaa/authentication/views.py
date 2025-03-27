from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Bem-vindo de volta!')
            return redirect('caaordserv')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')


