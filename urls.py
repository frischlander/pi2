from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('', include('caaordserv.urls')),
    path('sobre/', views.sobre, name='sobre'),
<<<<<<< HEAD
    path('two_factor/', include('two_factor.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
>>>>>>> a5d7afdc04631afdd0e4cd1501efff3df6336e88
