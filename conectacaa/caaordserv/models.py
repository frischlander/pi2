from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

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
        ultima_ordem = OrdemServico.objects.filter(processo__startswith='CAA').order_by('-processo').first()
        
        if ultima_ordem:
            # Extrai o número da última ordem (CAA000001 -> 000001)
            ultimo_numero = int(ultima_ordem.processo[3:])
            novo_numero = str(ultimo_numero + 1).zfill(6)
        else:
            novo_numero = '000001'
            
        return f'CAA{novo_numero}'

    processo = models.CharField(max_length=20, unique=True, editable=False)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nome_solicitante = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nao_iniciada')
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    justificativa_cancelamento = models.TextField(null=True, blank=True)
    parecer = models.TextField(null=True, blank=True, help_text="Parecer técnico para finalização da ordem de serviço")
    ultimo_usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Último Usuário')

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-processo']

    def __str__(self):
        return f"{self.processo} - {self.nome_solicitante}"

    def save(self, *args, **kwargs):
        if not self.processo:
            self.processo = self.gerar_numero_processo()
        super().save(*args, **kwargs)

    def get_processo_display(self):
        # Remove os zeros à esquerda do número, mantendo o prefixo CAA
        numero = str(int(self.processo[3:]))  # Converte para int para remover zeros à esquerda
        return f"CAA{numero}"

class AnexoOrdemServico(models.Model):
    ordem = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='ordens_servico/anexos/%Y/%m/%d/')
    descricao = models.CharField(max_length=200, blank=True)
    data_upload = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50, choices=[
        ('foto', 'Foto'),
        ('documento', 'Documento'),
        ('outro', 'Outro')
    ])

    class Meta:
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'
        ordering = ['-data_upload']

    def __str__(self):
        return f"Anexo {self.id} - {self.ordem.processo}"

    def delete(self, *args, **kwargs):
        # Remove o arquivo físico antes de deletar o registro
        if self.arquivo:
            self.arquivo.delete()
        super().delete(*args, **kwargs)
