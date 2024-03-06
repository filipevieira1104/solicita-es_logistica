from django.shortcuts import render
from solicitacao.models import Solicitacao
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required(login_url='/autenticacao/login/')
def recebido(request):
    cadastro = Solicitacao.objects.all().order_by('-id') # ordena sempre do mais recente para o mais antigo
    paginator = Paginator(cadastro, 6) # Mostrar 6 solicitações por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'recebimento.html', {'page_obj': page_obj})