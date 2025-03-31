from django.core.management.base import BaseCommand
from django.utils import timezone
from caaordserv.models import OrdemServico
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Cria dados de teste com datas diferentes para os relatórios'

    def handle(self, *args, **kwargs):
        # Tipos e status disponíveis
        tipos = ['atendimento_veterinario', 'denuncia_maus_tratos', 'castracao', 'captura_grande_porte']
        status = ['nao_iniciada', 'em_andamento', 'aguardando_parecer', 'finalizada', 'cancelada']
        
        # Nomes de teste
        nomes = [
            'João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa', 'Carlos Souza',
            'Julia Lima', 'Roberto Ferreira', 'Beatriz Almeida', 'Lucas Pereira', 'Fernanda Rodrigues'
        ]
        
        # Endereços de teste
        enderecos = [
            'Rua das Flores, 123', 'Avenida Principal, 456', 'Travessa do Sol, 789',
            'Rua do Comércio, 321', 'Avenida Central, 654', 'Rua das Palmeiras, 987'
        ]

        # Criar ordens para os últimos 3 anos
        for ano in range(3):
            ano_atual = timezone.now().year - ano
            self.stdout.write(f'Criando ordens para o ano {ano_atual}...')
            
            # Criar 20 ordens por ano
            for _ in range(20):
                # Gerar uma data aleatória para o ano atual
                dia = random.randint(1, 28)  # Evita problemas com fevereiro
                mes = random.randint(1, 12)
                hora = random.randint(0, 23)
                minuto = random.randint(0, 59)
                
                data_criacao = datetime(ano_atual, mes, dia, hora, minuto)
                
                ordem = OrdemServico.objects.create(
                    tipo=random.choice(tipos),
                    nome_solicitante=random.choice(nomes),
                    telefone=f'(11) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}',
                    endereco=random.choice(enderecos),
                    descricao=f'Ordem de teste criada em {data_criacao.strftime("%d/%m/%Y %H:%M")}',
                    status=random.choice(status),
                    data_criacao=data_criacao,
                    data_atualizacao=data_criacao + timedelta(days=random.randint(1, 30))
                )
                
                self.stdout.write(f'Criada ordem {ordem.processo} com data {data_criacao}')

        self.stdout.write(self.style.SUCCESS('Dados de teste criados com sucesso!')) 