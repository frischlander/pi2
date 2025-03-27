from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User

class UsernameValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        username=data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Nome de usuário não pode conter caracteres especiais'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Usuário já existe'}, status=409)
        return JsonResponse({'Usuário válido': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
        
