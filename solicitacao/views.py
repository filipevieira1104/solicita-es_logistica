from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Solicitacao
import re

@login_required(login_url='/autenticacao/login/')
def pedido(request):
    if request.method == 'GET':
        cadastro = Solicitacao.objects.all().order_by('-id') # ordena sempre do ma
        return render(request, 'solicitacao.html')
    elif request.method == 'POST':
        nome_solicitante = request.POST.get('nome_solicitante')
        nome_colaborador = request.POST.get('nome_colaborador')
        email = request.POST.get('email')
        num_chamado = request.POST.get('num_chamado')
        tipo = request.POST.get('tipo')
        produto = request.POST.get('produto')
        

        # Verifica se os campos de input estão vazios 
        if len(nome_solicitante.strip()) == 0 or len(nome_colaborador.strip()) == 0 or len(email.strip()) == 0 or len(num_chamado.strip()) == 0 or len(tipo.strip()) == 0 or len(produto.strip()) == 0:
            messages.add_message(request, messages.ERROR, 'Os campos não podem estar vazio !')
            return redirect('/solicitacao/pedido/')
        
        # valida se email corresponde ao dominio desejado 
        if not re.match(r'.*@speedlogi\.com$', email):
            messages.add_message(request, messages.WARNING, 'E-mail incorreto, Favor insira um e-mail SPEEDLOGI !')
            return redirect('/solicitacao/pedido/')
        
        # verifica se já existe uma solicitação com o número de chamado
        if Solicitacao.objects.filter(num_chamado = num_chamado).exists():
            messages.add_message(request, messages.WARNING, 'Já foi feito uma solicitação para esse chamado !')
            return redirect('/solicitacao/pedido/')
        
        # verifica se já foi feito uma solicitação de produto para aquele email
        if Solicitacao.objects.filter(email=email, produto=produto).exists():
            messages.add_message(request, messages.WARNING, f'produto já foi solicitado para colaborador(a) {nome_colaborador} !')
            return redirect('/solicitacao/pedido/')
        

        try:
            requisicao = Solicitacao(nome_solicitante = nome_solicitante,
                                     nome_colaborador = nome_colaborador,
                                     email = email,
                                     num_chamado = num_chamado,
                                     tipo = tipo,
                                     produto = produto)
            requisicao.save()
            messages.add_message(request, messages.SUCCESS, 'Solicitação enviada com sucesso !')
            return redirect('/solicitacao/pedido')
        except:
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema !')
            return redirect('/solicitacao/pedido')
    else:
        return redirect('/autenticacao/login/')
    
def atualizar_status(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        novo_status = request.POST.get('novo_status')
        solicitacao = Solicitacao.objects.get(pk=id)
        solicitacao.status = novo_status
        solicitacao.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Não está vindo como POST'})