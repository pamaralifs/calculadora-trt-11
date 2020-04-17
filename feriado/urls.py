from django.urls import path
from django.views.generic import TemplateView
from .views import *
# ou FeriadoCreate,FeriadoList,FeriadoUpdate,
# FeriadoDelete,FeriadoDetail

# Definir namespace como informado em urls projeto
app_name = 'feriado'

urlpatterns = [
    #path('',  TemplateView.as_view(template_name='feriado/index.html')),
    path('create/', FeriadoCreate.as_view(), name='feriado_create'),
    path('read/', FeriadoList.as_view(), name='feriado_read'),
    path('update/<int:pk>', FeriadoUpdate.as_view(), name='feriado_update'),
    path('delete/<int:pk>', FeriadoDelete.as_view(), name='feriado_delete'),
    path('detail/<int:pk>', FeriadoDetail.as_view(), name='feriado_detail'),
]