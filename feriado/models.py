from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

#https://stackoverflow.com/questions/52586623/django-createview-custom-validation
#https://docs.djangoproject.com/en/2.1/ref/validators/
#criando validação personalizada a ser usada no form a fim de usar nas views genéricas
def validate_weekend(value):
    if value.weekday() == 5:
        raise ValidationError(
            _('Informe uma data que não seja SÁBADO!'),
            params={'value': value},
        )
    elif value.weekday() == 6:
        raise ValidationError(
            _('Informe uma data que não seja DOMINGO!'),
            params={'value': value},
        )        

# Create your models here.
class Feriado(models.Model):
    data_feriado = models.DateField(validators=[validate_weekend],unique=True,verbose_name='DATA',help_text='Selecione um feriado ou dia não útil no formato: <em>AAAA-MM-DD</em>. ') 
    descricao = models.TextField(verbose_name='DESCRIÇÃO/MOTIVO')
    data_hora_cadastro = models.DateTimeField(auto_now_add=True)
    #data_hora_cadastro.editable = True
    #data_hora_cadastro = models.DateTimeField(default=timezone.now) não precisa, ele já considera o timezone no form
    data_hora_alteracao = models.DateTimeField(auto_now=True,editable=False)

    def __str__(self):
        return str(self.data_feriado)

