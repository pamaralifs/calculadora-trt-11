from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Feriado
from .forms import FeriadoFormCreateUpdate
# Create your views here.

class FeriadoCreate(CreateView):
    model = Feriado
    form_class = FeriadoFormCreateUpdate
    #fields = ['data_feriado', 'descricao',]
    success_url = reverse_lazy('feriado:feriado_read') 

class FeriadoUpdate(UpdateView):
    model = Feriado
    form_class = FeriadoFormCreateUpdate
    #fields = ['data_feriado', 'descricao',]
    success_url = reverse_lazy('feriado:feriado_read')

class FeriadoList(ListView):
    model = Feriado
    ordering = ['-data_feriado']  #mostrar da data mais recente para a mais antiga
    paginate_by = 3 # para o celular melhor 3 registros por página

    def get_context_data(self, **kwargs):
        total = super().get_context_data(**kwargs)
        total["total_registros"] = Feriado.objects.count()
        return total
    
class FeriadoDelete(DeleteView):
    model = Feriado
    success_url = reverse_lazy('feriado:feriado_read')


class FeriadoDetail(DetailView):
    model = Feriado
    fields = ['data_feriado', 'descricao',]
