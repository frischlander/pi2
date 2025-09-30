from django.contrib import admin
from .models import OrdemServico

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('processo', 'nome_solicitante', 'tipo', 'status', 'data_criacao')
    list_filter = ('tipo', 'status')
    search_fields = ('processo', 'nome_solicitante', 'endereco')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    ordering = ('-data_criacao',)
