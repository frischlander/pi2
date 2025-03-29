from django.shortcuts import render, redirect
from django.contrib import messages
from .models import OrdemServico

# Create your views here.
def index(request):
    return render(request,'caaordserv/index.html')

def add_ordem(request):
    if request.method == 'POST':
        try:
            ordem = OrdemServico.objects.create(
                processo=request.POST.get('processo'),
                tipo=request.POST.get('tipo'),
                nome_solicitante=request.POST.get('nome'),
                telefone=request.POST.get('telefone'),
                endereco=request.POST.get('endereco'),
                descricao=request.POST.get('descricao')
            )
            messages.success(request, 'Ordem de serviço criada com sucesso!')
            return redirect('caaordserv')
        except Exception as e:
            messages.error(request, f'Erro ao criar ordem de serviço: {str(e)}')
    
    return render(request, 'caaordserv/add_ordem.html')
