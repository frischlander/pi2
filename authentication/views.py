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
            # Redirecionar para verificação de 2FA se o usuário tiver 2FA habilitado
            if user.staticdevice_set.exists() or user.totpdevice_set.exists():
                return redirect('accounts:backup_tokens')  # Redireciona para verificação de 2FA
            messages.success(request, 'Bem-vindo de volta!')
            return redirect('caaordserv')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('accounts:login')


