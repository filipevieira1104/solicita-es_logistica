import re
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponse


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/solicitacao/pedido/')
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if len(nome.strip()) == 0 or len(email.strip()) == 0:
            messages.add_message(request, messages.ERROR, 'Nome, email e cargo não podem estar vazio !')
            return redirect('/autenticacao/cadastro/')
        
        if not re.match(r'.*@fractaliasystems\.es$', email):
            messages.add_message(request, messages.WARNING, 'E-mail incorreto, Favor insira um e-mail Fractalia !')
            return redirect('/autenticacao/cadastro/')
        
        if len(senha) < 8:
            messages.add_message(request, messages.ERROR, 'Sua senha deve ter no mínimo 8 caracteres !')
            return redirect('/autenticacao/cadastro/')
        
        if not re.search(r'[A-Z]', senha):
            messages.add_message(request, messages.WARNING, 'A senha deve conter pelo menos uma letra maiúscula !')
            return redirect('/autenticacao/cadastro/')
        
        if not re.search(r'[a-z]', senha):
            messages.add_message(request, messages.WARNING, 'A senha deve conter pelo menos uma letra minúscula !')
            return redirect('/autenticacao/cadastro/')
        
        if not re.search(r'\d', senha):
            messages.add_message(request, messages.WARNING, 'A senha deve conter pelo menos um número !')
            return redirect('/autenticacao/cadastro/')
        
        if not re.search(r'[!@#$%^&*()-_+=]', senha):
            messages.add_message(request, messages.WARNING, 'A senha deve conter pelo menos um caractere especial !')
            return redirect('/autenticacao/cadastro/')
        
        if User.objects.filter(email = email).exists():
            messages.add_message(request, messages.ERROR, 'E-mail já cadastrado !')
            return redirect('/autenticacao/cadastro/')
        
        if User.objects.filter(username = nome).exists():
            messages.add_message(request, messages.ERROR, 'Já existe um usuário com esse nome !')
            return redirect('/autenticacao/cadastro')
        
        try:
            pessoa = User.objects.create_user(username=nome, email=email, password=senha)
            pessoa.save()
            messages.add_message(request, messages.SUCCESS, 'Cadastro realizado com sucesso !')
            return redirect('/autenticacao/login/')
        except:
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema !')
            return redirect('/autenticacao/cadastro/')

def login(request):
    if request.user.is_authenticated:
        return redirect(request, '/solicitacao/pedido')
    return render(request, 'login.html')

def valida_login(request):
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')

    pessoa = auth.authenticate(request, username=nome, password=senha)

    if not pessoa:
        messages.add_message(request, messages.WARNING, 'Nome ou senha inválidos')
        return redirect('/autenticacao/login/')
    else:
        auth.login(request, pessoa)
        return redirect('/solicitacao/pedido/')


def sair(request):
    auth.logout(request)
    messages.add_message(request, messages.WARNING, 'Para acessar a plataforma, faça login novamente !')
    return redirect('/autenticacao/login/')    