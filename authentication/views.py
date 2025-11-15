from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserTwoFactorAuth
import json

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar se 2FA está habilitado
            try:
                two_factor = user.two_factor_auth
                if two_factor.is_enabled:
                    # Armazenar ID do usuário na sessão temporária
                    request.session['pre_2fa_user_id'] = user.id
                    messages.info(request, 'Digite seu código de autenticação')
                    return redirect('verify_2fa')
            except UserTwoFactorAuth.DoesNotExist:
                pass
            
            login(request, user)
            messages.success(request, 'Bem-vindo de volta!')
            return redirect('caaordserv')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return render(request, 'authentication/login.html')

class Verify2FAView(View):
    def get(self, request):
        if 'pre_2fa_user_id' not in request.session:
            return redirect('login')
        return render(request, 'authentication/verify_2fa.html')
    
    def post(self, request):
        if 'pre_2fa_user_id' not in request.session:
            return redirect('login')
        
        from django.contrib.auth.models import User
        user_id = request.session['pre_2fa_user_id']
        user = User.objects.get(id=user_id)
        
        token = request.POST.get('token', '').strip()
        backup_code = request.POST.get('backup_code', '').strip()
        
        two_factor = user.two_factor_auth
        
        # Tentar verificar token TOTP
        if token:
            if two_factor.verify_token(token):
                del request.session['pre_2fa_user_id']
                login(request, user)
                messages.success(request, 'Login bem-sucedido!')
                return redirect('caaordserv')
            else:
                messages.error(request, 'Código de autenticação inválido')
        
        # Tentar verificar código de backup
        if backup_code:
            if two_factor.verify_backup_code(backup_code):
                del request.session['pre_2fa_user_id']
                login(request, user)
                messages.warning(request, 'Código de backup usado. Gere novos códigos!')
                return redirect('caaordserv')
            else:
                messages.error(request, 'Código de backup inválido')
        
        return render(request, 'authentication/verify_2fa.html')

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('login')

@method_decorator(login_required, name='dispatch')
class Setup2FAView(View):
    def get(self, request):
        user = request.user
        two_factor, created = UserTwoFactorAuth.objects.get_or_create(user=user)
        
        if not two_factor.secret_key:
            two_factor.generate_secret()
            two_factor.save()
        
        context = {
            'qr_code': two_factor.get_qr_code_image(),
            'secret_key': two_factor.secret_key,
            'is_enabled': two_factor.is_enabled,
        }
        return render(request, 'authentication/setup_2fa.html', context)
    
    def post(self, request):
        user = request.user
        two_factor = user.two_factor_auth
        token = request.POST.get('token', '').strip()
        
        if not token or len(token) != 6:
            messages.error(request, 'Código inválido. Use 6 dígitos.')
            return redirect('setup_2fa')
        
        if two_factor.verify_token(token):
            two_factor.is_enabled = True
            backup_codes = two_factor.generate_backup_codes()
            two_factor.save()
            
            messages.success(request, 'Autenticação de dois fatores ativada!')
            
            context = {
                'backup_codes': backup_codes,
            }
            return render(request, 'authentication/backup_codes.html', context)
        else:
            messages.error(request, 'Código inválido. Tente novamente.')
            return redirect('setup_2fa')

@method_decorator(login_required, name='dispatch')
class Disable2FAView(View):
    def post(self, request):
        user = request.user
        try:
            two_factor = user.two_factor_auth
            two_factor.is_enabled = False
            two_factor.secret_key = ''
            two_factor.backup_codes = ''
            two_factor.save()
            messages.success(request, 'Autenticação de dois fatores desativada.')
        except UserTwoFactorAuth.DoesNotExist:
            pass
        
        return redirect('setup_2fa')


