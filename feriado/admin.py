from django.contrib import admin
from .models import Feriado
# Register your models here.

class FeriadoAdmin(admin.ModelAdmin):
    readonly_fields = ('data_hora_cadastro','data_hora_alteracao',)

#admin.site.register(Feriado)
admin.site.register(Feriado,FeriadoAdmin)