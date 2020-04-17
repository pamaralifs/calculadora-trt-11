from django import forms
from django.forms.widgets import TextInput

from feriado.models import Feriado


class DateInput(forms.DateInput): #CLASSE IA SER USADA ABAIXO em data_feriado para assumir widget html5 padrão
    input_type = 'date' #para poder abrir o calendário
    #placeholder = 'DD/MMm/aaaa' não funcionou
    #id='data_ciencia' a intenção era pegar o calendário do bootstrap mas não funcionou

class FeriadoFormCreateUpdate(forms.ModelForm):
    data_feriado = forms.DateField(label='DATA',error_messages = {
                'required': 'Informe a data!',
                'unique': 'Já existe um FERIADO cadastrado com esta DATA!'
    },widget=TextInput(attrs={'type':'date'}))
            #},widget=DateInput()) #label_suffix='' funciona no create mas não funciona no update
    descricao = forms.CharField(label='DESCRIÇÃO/MOTIVO',widget=forms.Textarea(attrs={'rows':'3','columns':'10'}))
    
    class Meta:
        model = Feriado
        exclude = ['id']
