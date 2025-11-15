from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django_otp.util import match_token


def otp_required(view_func):
    """
    Decorator que exige que o usuário tenha completado a verificação OTP (Two-Factor Authentication).
    Se o usuário não verificou OTP, redireciona para a verificação de 2FA.
    """
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapped_view(request, *args, **kwargs):
        # Verificar se o usuário tem algum dispositivo OTP habilitado
        if request.user.staticdevice_set.exists() or request.user.totpdevice_set.exists():
            # Verificar se já passou pela verificação de 2FA nesta sessão
            if not request.session.get('_otp_verified'):
                # Se não verificou 2FA, redirecionar para verificação
                return redirect('two_factor:backup_tokens')
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view
