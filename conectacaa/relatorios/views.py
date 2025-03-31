from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from caaordserv.models import OrdemServico
from django.db.models import Count
from django.db.models.functions import ExtractYear

@login_required
def index(request):
    # Obter o ano selecionado da URL ou usar o ano atual
    ano_selecionado = request.GET.get('ano')
    
    # Query base
    ordens = OrdemServico.objects.all()
    
    # Se um ano foi selecionado, filtrar por ele
    if ano_selecionado:
        ordens = ordens.filter(data_criacao__year=ano_selecionado)
    
    # Contagem de ordens por status
    status_counts = {
        'Não Iniciada': ordens.filter(status='nao_iniciada').count(),
        'Em Andamento': ordens.filter(status='em_andamento').count(),
        'Aguardando Parecer': ordens.filter(status='aguardando_parecer').count(),
        'Finalizada': ordens.filter(status='finalizada').count(),
        'Cancelada': ordens.filter(status='cancelada').count(),
    }

    # Contagem de ordens por tipo
    tipo_counts = {
        'Atendimento Veterinário': ordens.filter(tipo='atendimento_veterinario').count(),
        'Denúncia de Maus Tratos': ordens.filter(tipo='denuncia_maus_tratos').count(),
        'Castração': ordens.filter(tipo='castracao').count(),
        'Captura de Animais de Grande Porte': ordens.filter(tipo='captura_grande_porte').count(),
    }

    # Obter anos disponíveis para o dropdown
    anos_disponiveis = OrdemServico.objects.annotate(
        ano=ExtractYear('data_criacao')
    ).values('ano').distinct().order_by('-ano')

    context = {
        'status_data': {
            'labels': list(status_counts.keys()),
            'values': list(status_counts.values())
        },
        'tipo_data': {
            'labels': list(tipo_counts.keys()),
            'values': list(tipo_counts.values())
        },
        'anos_disponiveis': anos_disponiveis,
        'ano_selecionado': ano_selecionado
    }

    return render(request, 'relatorios/index.html', context) 