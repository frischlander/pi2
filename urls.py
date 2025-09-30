"""
URL configuration for conectacaa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
#from django.urls import path, include
#from django.conf import settings
#from django.conf.urls.static import static
#import views

#urlpatterns = [
#    path('admin/', admin.site.urls),
#    path('authentication/', include('authentication.urls')),
#    path('relatorios/', include('relatorios.urls')),
#    path('', include('caaordserv.urls')),
#    path('sobre/', views.sobre, name='sobre'),
#] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






# pi2/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import views

# Importações adicionais para gerenciamento programático
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth import get_user_model
import os # Importe o módulo os

# Função para criar o superusuário
def create_superuser_view(request ):
    User = get_user_model()
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'defaultpassword')

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        return HttpResponse(f"Superusuário '{username}' criado com sucesso!")
    return HttpResponse(f"Superusuário '{username}' já existe.")

# Função para aplicar migrações
def migrate_view(request):
    try:
        call_command('migrate')
        return HttpResponse("Migrações aplicadas com sucesso!")
    except Exception as e:
        return HttpResponse(f"Erro ao aplicar migrações: {e}", status=500)

urlpatterns = [
    # Adicione as novas URLs de gerenciamento no topo
    path('manage/migrate/', migrate_view, name='migrate'),
    path('manage/create_superuser/', create_superuser_view, name='create_superuser'),

    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('', include('caaordserv.urls')),
    path('sobre/', views.sobre, name='sobre'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

