from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from caaordserv.models import OrdemServico
from django.db.models import Count
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from django.http import HttpResponse

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

@login_required
def gerar_pdf_ordens(request):
    # Obtém os filtros da query string
    status = request.GET.get('status')
    tipo = request.GET.get('tipo')
    ano = request.GET.get('ano')
    
    # Inicia a query
    ordens = OrdemServico.objects.all()
    
    # Aplica os filtros
    if status:
        ordens = ordens.filter(status=status)
    if tipo:
        ordens = ordens.filter(tipo=tipo)
    if ano:
        ordens = ordens.filter(data_criacao__year=ano)
    
    # Ordena por data de criação (mais recentes primeiro)
    ordens = ordens.order_by('-data_criacao')
    
    # Cria o buffer para o PDF
    buffer = BytesIO()
    
    # Cria o documento PDF em formato paisagem
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )
    
    # Lista para armazenar os elementos do PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.alignment = TA_CENTER
    
    # Título
    title = "Relatório de Ordens de Serviço"
    if status:
        title += f" - Status: {status}"
    if tipo:
        title += f" - Tipo: {tipo}"
    if ano:
        title += f" - Ano: {ano}"
    
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 20))
    
    # Cabeçalho da tabela
    headers = [
        'ID', 'Tipo', 'Status', 'Data Criação', 'Data Finalização',
        'Endereço', 'Descrição', 'Observações'
    ]
    
    # Dados da tabela
    data = [headers]
    for ordem in ordens:
        data.append([
            ordem.get_processo_display(),
            ordem.get_tipo_display(),
            ordem.get_status_display(),
            ordem.data_criacao.strftime('%d/%m/%Y'),
            ordem.data_finalizacao.strftime('%d/%m/%Y') if ordem.data_finalizacao else '-',
            ordem.endereco,
            ordem.descricao,
            ordem.observacoes or '-'
        ])
    
    # Cria a tabela
    table = Table(data)
    
    # Estilo da tabela
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ])
    
    table.setStyle(style)
    elements.append(table)
    
    # Gera o PDF
    doc.build(elements)
    
    # Obtém o valor do buffer e cria a resposta
    pdf = buffer.getvalue()
    buffer.close()
    
    # Cria a resposta HTTP com o PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ordens_servico.pdf"'
    return response 