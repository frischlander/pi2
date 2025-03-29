from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import OrdemServico, AnexoOrdemServico
from .templates.pdf.ordem_servico_template import OrdemServicoTemplate
import os
from io import BytesIO
from datetime import datetime

# Create your views here.
def index(request):
    # Obtém os parâmetros de filtro da URL
    processo = request.GET.get('processo', '').strip()
    nome = request.GET.get('nome', '').strip()
    tipo = request.GET.get('tipo', '')
    endereco = request.GET.get('endereco', '').strip()
    status = request.GET.get('status', '')
    page = request.GET.get('page', '1')

    # Inicia a query
    ordens_list = OrdemServico.objects.all()

    # Aplica os filtros
    if processo:
        ordens_list = ordens_list.filter(processo__icontains=processo)
    if nome:
        ordens_list = ordens_list.filter(nome_solicitante__icontains=nome)
    if tipo:
        ordens_list = ordens_list.filter(tipo=tipo)
    if endereco:
        ordens_list = ordens_list.filter(endereco__icontains=endereco)
    if status:
        ordens_list = ordens_list.filter(status=status)

    # Ordena e aplica a paginação
    ordens_list = ordens_list.order_by('-data_criacao')
    paginator = Paginator(ordens_list, 10)
    
    try:
        ordens = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        ordens = paginator.page(1)
    
    # Contagem de ordens por status para os cards
    context = {
        'ordens': ordens,
        'total_finalizadas': ordens_list.filter(status='finalizada').count(),
        'total_em_andamento': ordens_list.filter(status='em_andamento').count(),
        'total_aguardando': ordens_list.filter(status='aguardando_parecer').count(),
        'total_canceladas': ordens_list.filter(status='cancelada').count(),
        'is_paginated': True,
        'page_obj': ordens,
        # Adiciona os valores dos filtros para manter o estado do formulário
        'filtros': {
            'processo': processo,
            'nome': nome,
            'tipo': tipo,
            'endereco': endereco,
            'status': status
        }
    }
    
    return render(request, 'caaordserv/index.html', context)

def add_ordem(request):
    if request.method == 'POST':
        try:
            ordem = OrdemServico.objects.create(
                tipo=request.POST.get('tipo'),
                nome_solicitante=request.POST.get('nome'),
                telefone=request.POST.get('telefone'),
                endereco=request.POST.get('endereco'),
                descricao=request.POST.get('descricao'),
                ultimo_usuario=request.user
            )
            
            # Processa os anexos
            if 'anexos' in request.FILES:
                for arquivo in request.FILES.getlist('anexos'):
                    AnexoOrdemServico.objects.create(
                        ordem=ordem,
                        arquivo=arquivo,
                        descricao=arquivo.name,
                        tipo='foto' if arquivo.content_type.startswith('image/') else 'documento'
                    )
            
            messages.success(request, f'Ordem de serviço {ordem.processo} criada com sucesso!')
            return redirect('caaordserv')
        except Exception as e:
            messages.error(request, f'Erro ao criar ordem de serviço: {str(e)}')
    
    # Gera o número do processo para visualização
    numero_processo = OrdemServico.gerar_numero_processo()
    return render(request, 'caaordserv/add_ordem.html', {'numero_processo': numero_processo})

def edit_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id)
    
    if request.method == 'POST':
        try:
            novo_status = request.POST.get('status')
            justificativa = request.POST.get('justificativa_cancelamento')
            parecer = request.POST.get('parecer')
            
            # Validação da justificativa quando o status é cancelada
            if novo_status == 'cancelada' and not justificativa:
                messages.error(request, 'É necessário informar uma justificativa para cancelar a ordem de serviço.')
                return render(request, 'caaordserv/edit_ordem.html', {'ordem': ordem})
            
            # Validação do parecer quando o status é finalizada
            if novo_status == 'finalizada' and not parecer:
                messages.error(request, 'É necessário informar um parecer técnico para finalizar a ordem de serviço.')
                return render(request, 'caaordserv/edit_ordem.html', {'ordem': ordem})
            
            ordem.tipo = request.POST.get('tipo')
            ordem.nome_solicitante = request.POST.get('nome')
            ordem.telefone = request.POST.get('telefone')
            ordem.endereco = request.POST.get('endereco')
            ordem.descricao = request.POST.get('descricao')
            ordem.status = novo_status
            ordem.justificativa_cancelamento = justificativa if novo_status == 'cancelada' else None
            ordem.parecer = parecer if novo_status == 'finalizada' else None
            ordem.ultimo_usuario = request.user
            ordem.save()
            
            # Processa os novos anexos
            if 'anexos' in request.FILES:
                for arquivo in request.FILES.getlist('anexos'):
                    AnexoOrdemServico.objects.create(
                        ordem=ordem,
                        arquivo=arquivo,
                        descricao=arquivo.name,
                        tipo='foto' if arquivo.content_type.startswith('image/') else 'documento'
                    )
            
            messages.success(request, f'Ordem de serviço {ordem.processo} atualizada com sucesso!')
            return redirect('caaordserv')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar ordem de serviço: {str(e)}')
    
    return render(request, 'caaordserv/edit_ordem.html', {'ordem': ordem})

def delete_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id)
    try:
        ordem.delete()
        messages.success(request, f'Ordem de serviço {ordem.processo} excluída com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir ordem de serviço: {str(e)}')
    
    return redirect('caaordserv')

def view_ordem(request, ordem_id):
    try:
        ordem = get_object_or_404(OrdemServico, id=ordem_id)
        return render(request, 'caaordserv/view_ordem.html', {'ordem': ordem})
    except Exception as e:
        messages.error(request, f'Erro ao carregar ordem de serviço: {str(e)}')
        return redirect('caaordserv')

def delete_anexo(request, anexo_id):
    anexo = get_object_or_404(AnexoOrdemServico, id=anexo_id)
    ordem_id = anexo.ordem.id
    try:
        anexo.delete()
        messages.success(request, 'Anexo excluído com sucesso!')
    except Exception as e:
        messages.error(request, f'Erro ao excluir anexo: {str(e)}')
    
    return redirect('edit_ordem', ordem_id=ordem_id)

def download_anexo(request, anexo_id):
    anexo = get_object_or_404(AnexoOrdemServico, id=anexo_id)
    try:
        return FileResponse(anexo.arquivo, as_attachment=True)
    except Exception as e:
        messages.error(request, f'Erro ao baixar anexo: {str(e)}')
        return redirect('edit_ordem', ordem_id=anexo.ordem.id)

def gerar_pdf_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id)
    
    # Criar um buffer para armazenar o PDF
    buffer = BytesIO()
    
    # Criar o template e gerar o PDF
    template = OrdemServicoTemplate(buffer)
    template.build(ordem)
    
    # Criar a resposta para exibir o PDF
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="ordem_servico_{ordem.processo}.pdf"'
    return response
