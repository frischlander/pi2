from django.db import models
from django.utils import timezone

class OrdemServico(models.Model):
    TIPO_CHOICES = [
        ('atendimento_veterinario', 'Atendimento Veterinário'),
        ('denuncia_maus_tratos', 'Denúncia de Maus Tratos'),
        ('resgate', 'Resgate de Animais'),
        ('outros', 'Outros'),
    ]

    STATUS_CHOICES = [
        ('aguardando_parecer', 'Aguardando Parecer'),
        ('em_andamento', 'Em Andamento'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]

    processo = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nome_solicitante = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aguardando_parecer')
    data_criacao = models.DateTimeField(default=timezone.now)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-data_criacao']

    def __str__(self):
        return f"{self.processo} - {self.nome_solicitante}"
