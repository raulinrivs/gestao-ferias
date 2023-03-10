from django.db import models
import datetime
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
        matricula = models.CharField(max_length=15, verbose_name='Matricula', unique=True)
        data_admissao = models.DateField(verbose_name='Data de admissão', default=datetime.date.today())
        gestor = models.ManyToManyField(Group, blank=True)
        

class Solicitacao(models.Model):
        class Meta:
                verbose_name_plural = "Solicitações"
        
        TIPO_FERIAS = [
                ('INT', 'Integral'), 
                ('VEN', 'Venda'), 
                ('PAR', 'Parcial'),
        ]
        STATUS = [
                ('CRI', 'Criada'),
                ('VGE', 'Validada pelo Gestor'),
                ('RGE', 'Recusada pelo Gestor'),
                ('DEF', 'Deferido'),
                ('RRH', 'Recusada pelo RH'),
                ('CON', 'Concluida'),
        ]
        status = models.CharField(choices=STATUS, max_length=3)
        tipo_ferias = models.CharField(choices=TIPO_FERIAS, max_length=3)
        intervalos = models.TextField()
        solicitante = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
        
        def __str__(self) -> str:
                return f'{self.tipo_ferias} - {self.status} - {self.solicitante}'
