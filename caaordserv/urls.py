from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='caaordserv'),
    path('add-ordem/', views.add_ordem, name='add_ordem'),
    re_path(r'^edit-ordem/(?P<processo>[^/]+(?:/[^/]+)?)/$', views.edit_ordem, name='edit_ordem'),
    re_path(r'^delete-ordem/(?P<processo>[^/]+(?:/[^/]+)?)/$', views.delete_ordem, name='delete_ordem'),
    re_path(r'^view-ordem/(?P<processo>[^/]+(?:/[^/]+)?)/$', views.view_ordem, name='view_ordem'),
    path('delete-anexo/<int:anexo_id>/', views.delete_anexo, name='delete_anexo'),
    path('download-anexo/<int:anexo_id>/', views.download_anexo, name='download_anexo'),
    re_path(r'^gerar-pdf/(?P<processo>[^/]+(?:/[^/]+)?)/$', views.gerar_pdf_ordem, name='gerar_pdf_ordem'),
    path('gerar-pdf-lista/', views.gerar_pdf_lista, name='gerar_pdf_lista'),
]