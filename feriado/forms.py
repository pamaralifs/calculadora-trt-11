from django import forms
from django.forms.widgets import TextInput
from feriado.models import Feriado, validate_weekend, validate_dia_nao_util

class DateInput(forms.DateInput): #CLASSE IA SER USADA ABAIXO em data_feriado para assumir widget html5 padrão
    input_type = 'date' #para poder abrir o calendário
    #placeholder = 'DD/MMm/aaaa' não funcionou
    #id='data_ciencia' a intenção era pegar o calendário do bootstrap mas não funcionou

#FORM DO CRUD
class FeriadoFormCreateUpdate(forms.ModelForm):
    data_feriado = forms.DateField(validators=[validate_weekend],label='DATA',error_messages = {
                'required': 'Informe a data!',
                'unique': 'Já existe um FERIADO (ou dia não útil) cadastrado com esta DATA!'
    },widget=TextInput(attrs={'type':'date'}))
            #},widget=DateInput()) #label_suffix='' funciona no create mas não funciona no update
    descricao = forms.CharField(label='DESCRIÇÃO/MOTIVO',widget=forms.Textarea(attrs={'rows':'3','columns':'10'}))
    
    class Meta:
        model = Feriado
        exclude = ['id']
    
#FORM DO INDEX
class FormCalcular(forms.Form):
    data_ciencia = forms.DateField(validators=[validate_dia_nao_util],label='Data de ciência',widget=forms.TextInput(attrs={'type':'date','id':'data_ciencia','class':'form-control','placeholder':'(Data de ciência)'})) #precisou colocar o id por causa do datapicker
    qtd_dias = forms.IntegerField(label='Quantidade de dias para contagem',min_value=1,widget=forms.NumberInput(attrs={'':'','class':'form-control','placeholder':'(Qtde dias)'}))
    #
    # def clean_data_ciencia(self):
    #    data = self.cleaned_data.get("data_ciencia")
    #    print("data:",data)
    #    q = Feriado.objects.filter(data_feriado = data)
    #    print("q:",q)        
    #    #if not "yourdomain.com" in email_passed:
    #    if q:
    #        raise forms.ValidationError(q,"Sorry, the email submitted is invalid. All emails have to be registered on this domain only.")
    #    return data

#FORM FILTRO BUSCA
DIA_CHOICES = [('','')]
DIA_CHOICES += [(dia, dia) for dia in range(1, 32)]
MES_CHOICES = [('',''),('01','Janeiro'),('02','Fevereiro'),('03','Março'),('04','Abril'),('05','Maio'),('06','Junho'),
    ('07','Julho'),('08','Agosto'),('09','Setembro'),('10','Outubro'),('11','Novembro'),('12','Dezembro')]
#months = [(month, month) for month in range(1, 13)]
#ANO_CHOICES = [(ano, ano) for ano in [2018, 2019, 2020]]
class FormBusca(forms.Form):
    #required=False
    #dia = forms.ChoiceField(label='Dia',choices=DIA_CHOICES,initial='',widget=forms.Select(attrs={'class':'form-control','style':'width:70px'}))
    mes = forms.ChoiceField(label='Mês',choices=MES_CHOICES,initial='',required=False,widget=forms.Select(attrs={'class':'form-control','style':'width:123px'}))
    ano = forms.IntegerField(label='Ano',min_value=1900,max_value=2100,error_messages={
                'required': 'Informe o ano com 4 dígitos!'},widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'aaaa','style':'width:75px'}))
    #ano É DE PREENCHIMENTO OBRIGATÓRIO, ou seja, não tem required=False
