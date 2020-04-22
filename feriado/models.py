from django.db import models
from django.core.exceptions import ValidationError  # para usar nas funções de valicação
from django.utils.translation import ugettext_lazy as _  # para usar nas funções de valicação

#https://stackoverflow.com/questions/52586623/django-createview-custom-validation
#https://docs.djangoproject.com/en/2.1/ref/validators/
# VALIDATORS - FUNÇÕES DE VALIDAÇÃO PERSONALIZADAS PARA USAR NESTE MODEL (QUE TABÉM É AUTOMATICAMENTE
# IMPLICITAMENTE INVOCADA PELOS MODELFORMS)

# Criando validação personalizada para ser usada no models.py e implicitamente no form CRUD das views CBV Create e Update
# Neste validator não precisa checar se é um feriado/dia não útil já cadastrado porque a restrição
# "unique=" do model já cria um validate para isso.
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

# CRIAÇÃO DE UM ARQUIVO SEPARADO DE VALIDATORS PARA USAR EM FORMS (MAIS NÃO FUNCIONOU NESTE CASO porque precisa do objeto Feriado)
# https://django.cowhite.com/blog/django-form-validation-and-customization-adding-your-own-validation-rules/
# criando validação personalizada para usar no form FormCalcular (calcular prazo) ou
# em qualquer outro form, a fim de impossibilitar que um feriado ou data não útil seja tomada
# como "data de ciência" num form submmit       
def validate_dia_nao_util(value):
    q = Feriado.objects.filter(data_feriado = value)
    print("q in validators:",q)
    if q:
        #print("q in validators:",q)
        raise ValidationError(
             _('A DATA DE CIÊNCIA não pode ser um FERIADO (ou dia não útil) já cadastrado!'),
            params={'value': value},
        )
    elif value.weekday() == 5:
        raise ValidationError(
            _('A DATA DE CIÊNCIA não pode ser um SÁBADO!'),
            params={'value': value},
        )
    elif value.weekday() == 6:
        raise ValidationError(
            _('A DATA DE CIÊNCIA não pode ser um DOMINGO!'),
            params={'value': value},
        )

# MODELOS da app feriado
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

