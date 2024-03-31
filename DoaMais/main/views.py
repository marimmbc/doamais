from django.shortcuts import render

def login(request):
    return render(request, 'login.html')

def cadastrar(request):
    return render(request, 'cadastrar.html')

def entrar(request):
    return render(request, 'entrar.html')

def perfil(request):
    return render(request, 'perfil.html')

def editar_perfil(request):
    return render(request, 'editar_perfil.html')

def pesquisar(request):
    return render(request, 'pesquisar.html')

def solicitar_item(request):
    return render(request, 'solicitar_item.html')

def itens_solicitados(request):
    return render(request, 'itens_solicitados.html')

def doar_item(request):
    return render(request, 'doar_item.html')

def minhas_doacoes(request):
    return render(request, 'minhas_doacoes.html')

def editar_doacao(request):
    return render(request, 'editar_doacao.html')