from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from caaordserv.models import OrdemServico
from django.db.models import Count
from django.db.models.functions import ExtractYear

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

    # Obter anos disponíveis
    anos = OrdemServico.objects.annotate(ano=ExtractYear('data_criacao')).values('ano').distinct().order_by('-ano')
    anos = [ano['ano'] for ano in anos]

    # Dados por ano
    dados_por_ano = {}
    for ano in anos:
        ordens_ano = OrdemServico.objects.filter(data_criacao__year=ano)
        
        # Status por ano
        status_counts_ano = {
            'Não Iniciada': ordens_ano.filter(status='nao_iniciada').count(),
            'Em Andamento': ordens_ano.filter(status='em_andamento').count(),
            'Aguardando Parecer': ordens_ano.filter(status='aguardando_parecer').count(),
            'Finalizada': ordens_ano.filter(status='finalizada').count(),
            'Cancelada': ordens_ano.filter(status='cancelada').count(),
        }

        # Tipo por ano
        tipo_counts_ano = {
            'Atendimento Veterinário': ordens_ano.filter(tipo='atendimento_veterinario').count(),
            'Denúncia de Maus Tratos': ordens_ano.filter(tipo='denuncia_maus_tratos').count(),
            'Castração': ordens_ano.filter(tipo='castracao').count(),
            'Captura de Animais de Grande Porte': ordens_ano.filter(tipo='captura_grande_porte').count(),
        }

        dados_por_ano[ano] = {
            'status': {
                'labels': list(status_counts_ano.keys()),
                'values': list(status_counts_ano.values())
            },
            'tipo': {
                'labels': list(tipo_counts_ano.keys()),
                'values': list(tipo_counts_ano.values())
            }
        }

    context = {
        'status_data': {
            'labels': list(status_counts.keys()),
            'values': list(status_counts.values())
        },
        'tipo_data': {
            'labels': list(tipo_counts.keys()),
            'values': list(tipo_counts.values())
        },
        'anos': anos,
        'dados_por_ano': dados_por_ano
    }

    return render(request, 'relatorios/index.html', context) 