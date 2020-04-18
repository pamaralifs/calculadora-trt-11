from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView,TemplateView
from django.views.generic.edit import FormView
from .models import Feriado
from .forms import FeriadoFormCreateUpdate, FormCalcular
#from django.utils import dateparse
import datetime
# Create your views here.

#VISTAS CRUDDs
#CREATE
class FeriadoCreate(CreateView):
    model = Feriado
    form_class = FeriadoFormCreateUpdate
    #fields = ['data_feriado', 'descricao',]
    success_url = reverse_lazy('feriado:feriado_read') 

#READ
class FeriadoList(ListView):
    model = Feriado
    ordering = ['-data_feriado']  #mostrar da data mais recente para a mais antiga
    paginate_by = 3 # para o celular melhor 3 registros por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_registros"] = Feriado.objects.count()
        return context
#UPDATE 
class FeriadoUpdate(UpdateView):
    model = Feriado
    form_class = FeriadoFormCreateUpdate
    #fields = ['data_feriado', 'descricao',]
    success_url = reverse_lazy('feriado:feriado_read')
#DELETE
class FeriadoDelete(DeleteView):
    model = Feriado
    success_url = reverse_lazy('feriado:feriado_read')

#DETAIL
class FeriadoDetail(DetailView):
    model = Feriado
    fields = ['data_feriado', 'descricao',]
    

#VISTAS REGRAS DO NEGÓCIO
#INDEX
class FeriadoCalcularDataExpiracao(FormView):
    form_class = FormCalcular
    template_name = "feriado/index.html"
    model = Feriado
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FormCalcular # Insere o form no contexto do template
        #print('TESTE',self.request.GET.get('email'))
        data_ciencia = self.request.GET.get('data_ciencia')
        qtd_dias = self.request.GET.get('qtd_dias')
        #-------------------
        DIAS = ['Segunda-feira','Terça-feira','Quarta-feira','Quinta-Feira','Sexta-feira','Sábado','Domingo']
        lista_dias = []
        lista_feriados = []
        #pega dados do formulário web submetido pelo internauta
        data_ciencia = self.request.GET.get('data_ciencia', '')
        qtd_dias = self.request.GET.get('qtd_dias', '')
        #print('data ciencia:',data_ciencia)
        #inicializa mensagem de erro
        context['mensagem_erro'] = ''
        if not data_ciencia.strip() or not qtd_dias.strip(): #or dateparse.parse_date(data_ciencia):
            context['mensagem_erro'] = 'Preencha os campos do formulário no menu acima!'
            # Retorna queryset vazio 
            # lista_feriados = Feriado.objects.none()
        else:
            qtd_dias = int(qtd_dias)
            #necessário converter a data_ciencia para o tipo date
            #data_ciencia = datetime.strptime('17/04/2020', '%d/%m/%Y')
            #converte para o tipo datetime
            data_ciencia = datetime.datetime.strptime(data_ciencia, '%Y-%m-%d')
            #agora converte para o tipo date
            data_ciencia = datetime.datetime.date(data_ciencia)
            #consultar a tabela feriado do banco e realizar contagem
            #q = Feriado.objects.filter(data_feriado__gt = data_ciencia)
            contador = 0
            #https://www.vivaolinux.com.br/dica/Manipulando-data-e-hora-em-Python-com-timedelta
            #https://groups.google.com/forum/#!topic/python-brasil/Jp0YhDe6Hzk
            #soma 1 dia a data de ciência (começa a contar 1 dia depois da data de ciência)
            #o dia seguinte, ou seja, data buscacontinua sendo só tipo date (e não datetime)
            data_busca = data_ciencia
            lista_dias.append('<span style="color:red">' + data_busca.strftime('%d/%m/%Y') + ' - ' + DIAS[data_busca.weekday()] + ' (Data de ciência)</span>')
            while contador < qtd_dias:
                data_busca = data_busca + datetime.timedelta(days=1)
                #https://dicasdepython.com.br/python-como-identificar-o-dia-da-semana-de-uma-data/
                #https://pt.stackoverflow.com/questions/270271/python3-como-calcular-o-n%C3%BAmero-de-dias-%C3%BAteis-entre-duas-datas
                #não conta final de semana (dia não útil)
                #if 0 =< data_busca.weekday() <= 4:
                #print('entrei no loop')
                q = Feriado.objects.filter(data_feriado = data_busca)
                if (data_busca.weekday() not in (5, 6)) and (not q):
                    #verifica se a data_busca é final de semana (5=sábado,6=domingo)
                    #verifica se esse dia existe na tabela de feriados
                    #Feriado.objects.get(data_feriado = data_busca) dá erro se não encontrar
                    #por isso usei filtro, pois retorna queryset vazio se não encontrar
                    #portanto, se não é final de semana e não é feriado, então incrementa
                    # a data e o contador, contando como data útil válida
                    contador += 1
                    #print(contador,') data busca',data_busca)
                    lista_dias.append('<strong>(' + str(contador) + 'º dia)</strong> - ' + data_busca.strftime('%d/%m/%Y') + ' - ' + DIAS[data_busca.weekday()])
                else:
                    # monta lista de datas de finais de semana
                    #print(' ---> data busca',data_busca,DIAS[data_busca.weekday()])
                    if data_busca.weekday() in (5, 6):
                        lista_dias.append('<span style="color:red">' + data_busca.strftime('%d/%m/%Y') + ' - ' + DIAS[data_busca.weekday()] + '</span>')
                    else:
                        lista_dias.append('<span style="color:red">' + data_busca.strftime('%d/%m/%Y') + ' - ' + DIAS[data_busca.weekday()] + ' ('+ q[0].descricao +')</span>')
                    #incrementa a data de busca em mais um dia
                
            # monta as demais variáveis de contexto
            # monta lista de feriados arrolados durante o período entre a data de ciência
            # e a data de expiração, ao sair do loop da contagem de dias
            feriados = Feriado.objects.filter(data_feriado__gt = data_ciencia,data_feriado__lte = data_busca)
            for obj in feriados:
                lista_feriados.append(obj.data_feriado.strftime('%d/%m/%Y') + ' - ' + DIAS[obj.data_feriado.weekday()])
            # data de expiração que é a última data de busca convertida para string
            context['data_expiracao'] = data_busca.strftime('%d/%m/%Y')
            # lista de finais de semana no período entre data ciência e data expiração
            context['lista_dias'] = lista_dias           
            # lista de feriados no período entre data ciência e data expiração
            context['lista_feriados'] = lista_feriados
            # devolve data ciência
            context['data_ciencia'] = data_ciencia.strftime('%d/%m/%Y')
            # devolve quantidade de dias de contagem
            context['qtd_dias'] = qtd_dias            
        return context
            #https://pt.stackoverflow.com/questions/94523/filtro-por-data-em-lista-django
            #q=Job.objects.filter(data_job__range=(start_date,end_date))
            #p = p.filter(data_job__lte=dmin,data_job__gte=dmax)
            #for i in q:
            #    i.nome_job, i.data_job
            #Você deve converter a sua data antes da pesquisa:
            #from datetime import datetime
            #min_date = datetime.strptime(dmin, "%d/%m/%Y")
            #max_date = datetime.strptime(dmax, "%d/%m/%Y")
            # = p.filter(data_job__gte=min_date,data_job__lte=max_date) ou
            # = p.filter(data_job__gt=min_date,data_job__lte=max_date)
    


        
        
        

