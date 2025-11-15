from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # <-- CORREÇÃO: Importar views do projeto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('two_factor.urls')),
    path('authentication/', include('authentication.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('sobre/', views.sobre, name='sobre'),  # <-- CORREÇÃO: Adicionada a view
    path('', include('caaordserv.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)