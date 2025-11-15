from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
import views

# Importações do two_factor para incluir manualmente
from two_factor.views import (
    LoginView, SetupView, SetupCompleteView, BackupTokensView,
    PhoneSetupView, PhoneDeleteView, DisableView, ProfileView
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Two Factor Auth - URLs manuais para evitar regex
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/setup/', SetupView.as_view(), name='setup'),
    path('account/setup/complete/', SetupCompleteView.as_view(), name='setup_complete'),
    path('account/backup/tokens/', BackupTokensView.as_view(), name='backup_tokens'),
    path('account/profile/', ProfileView.as_view(), name='profile'),
    path('account/disable/', DisableView.as_view(), name='disable'),
    
    # Fallback para outras URLs do two_factor (se necessário)
    path('account/', include('two_factor.urls')),
    
    # Authentication customizado
    path('authentication/', include('authentication.urls')),
    
    # Outras URLs
    path('relatorios/', include('relatorios.urls')),
    path('', include('caaordserv.urls')),
    path('sobre/', views.sobre, name='sobre'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)