from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Esta é a linha correta para a autenticação de dois fatores
    path('account/', include(('two_factor.urls', 'two_factor'))),
    
    # Suas outras rotas
    path('authentication/', include('authentication.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('', include('caaordserv.urls')),
    path('sobre/', views.sobre, name='sobre'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)