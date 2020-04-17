from django.db import models
from django.utils import timezone


# Create your models here.
class Feriado(models.Model):
    data_feriado = models.DateField(unique=True,verbose_name='DATA',help_text='Selecione um feriado ou dia não útil no formato: <em>AAAA-MM-DD</em>. ') 
    descricao = models.TextField(verbose_name='DESCRIÇÃO/MOTIVO')
    data_hora_cadastro = models.DateTimeField(auto_now_add=True)
    #data_hora_cadastro.editable = True
    #data_hora_cadastro = models.DateTimeField(default=timezone.now) não precisa, ele já considera o timezone no form
    data_hora_alteracao = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self):
        return str(self.data_feriado)

