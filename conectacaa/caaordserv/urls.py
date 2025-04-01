from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='caaordserv'),
    path('add-ordem/', views.add_ordem, name='add_ordem'),
    path('edit-ordem/<int:ordem_id>/', views.edit_ordem, name='edit_ordem'),
    path('delete-ordem/<int:ordem_id>/', views.delete_ordem, name='delete_ordem'),
    path('view-ordem/<int:ordem_id>/', views.view_ordem, name='view_ordem'),
    path('delete-anexo/<int:anexo_id>/', views.delete_anexo, name='delete_anexo'),
    path('download-anexo/<int:anexo_id>/', views.download_anexo, name='download_anexo'),
    path('gerar-pdf/<int:ordem_id>/', views.gerar_pdf_ordem, name='gerar_pdf_ordem'),
    path('gerar-pdf-lista/', views.gerar_pdf_lista, name='gerar_pdf_lista'),
]