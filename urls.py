from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importação correta da view
from caaordserv.views import sobre

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('two_factor.urls')),
    path('authentication/', include('authentication.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('', include('caaordserv.urls')),
    path('sobre/', sobre, name='sobre'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)