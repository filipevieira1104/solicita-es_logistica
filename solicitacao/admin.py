from django.contrib import admin
from .models import Solicitacao

@admin.register(Solicitacao)
class FormRequisicaoModel(admin.ModelAdmin):
    list_display = ('nome_solicitante',
                    'nome_colaborador',
                    'email',
                    'num_chamado',
                    'data_solicitacao',
                    'tipo',
                    'produto',
                    'status')   
    search_fields = ['status', 'nome_colaborador', 'email', 'produto', 
                     'num_chamado', 'data_solicitacao']

    