from django.db import models
from django.utils import timezone

class Solicitacao(models.Model):
    nome_solicitante = models.CharField(max_length=100)
    nome_colaborador = models.CharField(max_length=100)
    email = models.EmailField()
    num_chamado = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    produto = models.CharField(max_length=100)
    
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Em andamento', 'Em andamento'),
        ('Atendido', 'Atendido')
    )
    status = models.CharField(max_length=100, choices = STATUS_CHOICES, default='Pendente')
    data_solicitacao = models.DateField()

    def save(self, *args, **kwargs):
        if not self.data_solicitacao:
            self.data_solicitacao = timezone.now().date()
        super(Solicitacao, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome_colaborador