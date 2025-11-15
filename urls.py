from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from caaordserv import views

# Importações adicionais para gerenciamento programático
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth import get_user_model
import os # Importe o módulo os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('two_factor.urls')),
    path('authentication/', include('authentication.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('', include('caaordserv.urls')),
    path('sobre/', views.sobre, name='sobre'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)