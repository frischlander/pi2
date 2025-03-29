from django.db import models
from django.utils import timezone
from datetime import datetime

class OrdemServico(models.Model):
    TIPO_CHOICES = [
        ('atendimento_veterinario', 'Atendimento Veterinário'),
        ('denuncia_maus_tratos', 'Denúncia de Maus Tratos'),
        ('castracao', 'Castração'), 
        ('captura_grande_porte', 'Captura de Animais de Grande Porte'),              
    ]

    STATUS_CHOICES = [
        ('nao_iniciada', 'Não Iniciada'),        
        ('em_andamento', 'Em Andamento'),
        ('aguardando_parecer', 'Aguardando Parecer'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    @staticmethod
    def gerar_numero_processo():
        data_atual = datetime.now().strftime('%d%m%Y')
        ultima_ordem = OrdemServico.objects.filter(processo__startswith='CAA').order_by('-processo').first()
        
        if ultima_ordem:
            # Extrai o número da última ordem (CAA001 -> 001)
            ultimo_numero = int(ultima_ordem.processo.split('/')[0][3:])
            novo_numero = str(ultimo_numero + 1).zfill(3)
        else:
            novo_numero = '001'
            
        return f'CAA{novo_numero}/{data_atual}'

    processo = models.CharField(max_length=20, unique=True, editable=False)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nome_solicitante = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_iniciada')
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.processo} - {self.nome_solicitante}"

    def save(self, *args, **kwargs):
        if not self.processo:
            self.processo = self.gerar_numero_processo()
        super().save(*args, **kwargs)
