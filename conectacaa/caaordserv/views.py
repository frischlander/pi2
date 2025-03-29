from django.shortcuts import render, redirect
from django.contrib import messages
from .models import OrdemServico

# Create your views here.
def index(request):
    ordens = OrdemServico.objects.all().order_by('-data_criacao')
    
    # Contagem de ordens por status para os cards
    context = {
        'ordens': ordens,
        'total_finalizadas': ordens.filter(status='finalizada').count(),
        'total_em_andamento': ordens.filter(status='em_andamento').count(),
        'total_aguardando': ordens.filter(status='aguardando_parecer').count(),
        'total_canceladas': ordens.filter(status='cancelada').count(),
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
                descricao=request.POST.get('descricao')
            )
            messages.success(request, f'Ordem de serviço {ordem.processo} criada com sucesso!')
            return redirect('caaordserv')
        except Exception as e:
            messages.error(request, f'Erro ao criar ordem de serviço: {str(e)}')
    
    return render(request, 'caaordserv/add_ordem.html')
