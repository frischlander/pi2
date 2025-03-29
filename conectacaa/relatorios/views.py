from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from caaordserv.models import OrdemServico

@login_required
def index(request):
    # Contagem de ordens por status
    status_counts = {
        'Não Iniciada': OrdemServico.objects.filter(status='nao_iniciada').count(),
        'Em Andamento': OrdemServico.objects.filter(status='em_andamento').count(),
        'Aguardando Parecer': OrdemServico.objects.filter(status='aguardando_parecer').count(),
        'Finalizada': OrdemServico.objects.filter(status='finalizada').count(),
        'Cancelada': OrdemServico.objects.filter(status='cancelada').count(),
    }

    # Contagem de ordens por tipo
    tipo_counts = {
        'Atendimento Veterinário': OrdemServico.objects.filter(tipo='atendimento_veterinario').count(),
        'Denúncia de Maus Tratos': OrdemServico.objects.filter(tipo='denuncia_maus_tratos').count(),
        'Castração': OrdemServico.objects.filter(tipo='castracao').count(),
        'Captura de Animais de Grande Porte': OrdemServico.objects.filter(tipo='captura_grande_porte').count(),
    }

    context = {
        'status_data': {
            'labels': list(status_counts.keys()),
            'values': list(status_counts.values())
        },
        'tipo_data': {
            'labels': list(tipo_counts.keys()),
            'values': list(tipo_counts.values())
        }
    }

    return render(request, 'relatorios/index.html', context) 