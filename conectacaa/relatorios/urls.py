from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.index, name='index'),
    path('gerar-pdf-ordens/', views.gerar_pdf_ordens, name='gerar_pdf_ordens'),
] 