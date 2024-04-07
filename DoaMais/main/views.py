from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib import messages

from .models import Doacao, SolicitarItem, User

def inicio(request):
    return render(request, 'inicio.html')

def cadastrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                user = authenticate(username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('pesquisar')
            except Exception as e:
                return HttpResponse(str(e))
        else:
            return HttpResponse("As senhas não coincidem ou outro erro de validação.")
    return render(request, 'cadastrar.html')

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('pesquisar')
    else:
        messages.error(request, 'Invalid username or password!')
    return render(request, 'login.html')


@login_required
def perfil(request):
    user = request.user
    return render(request, 'perfil.html', {'user': user})

@login_required
def editar_perfil(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        # Atualize outros campos conforme necessário

        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']

        user.save()
        return redirect('perfil')  # Redirecione para a página do perfil ou outra página conforme necessário

    return render(request, 'editar_perfil.html', {'user': user})

@login_required
def pesquisar(request):
    query = request.GET.get('title')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    resultados = Doacao.objects.all()

    if query:
        resultados = resultados.filter(item_name__icontains=query)
    if category:
        resultados = resultados.filter(category=category)
    if condition:
        resultados = resultados.filter(condition=condition)

    return render(request, 'pesquisar.html', {'resultados': resultados})

@login_required
def solicitar_item(request):
    if request.method == 'POST':
        form_data = request.POST
        image = request.FILES.get('image')

        novo_item = SolicitarItem(
            title=form_data['title'],
            category=form_data['category'],
            condition=form_data['condition'],
            description=form_data['description'],
            image=image
        )
        novo_item.save()

        return redirect('itens_solicitados')  # Redireciona para a página de itens solicitados após o cadastro

    return render(request, 'solicitar_item.html')

@login_required
def itens_solicitados(request):
    itens = SolicitarItem.objects.all()  # Recupera todos os itens solicitados
    return render(request, 'itens_solicitados.html', {'itens': itens})

@login_required
def doar_item(request):
    if request.method == 'POST':
        new_donation = Doacao(
            item_name=request.POST.get('item_name'),
            category=request.POST.get('category'),
            condition=request.POST.get('condition'),
            image=request.FILES.get('image') if 'image' in request.FILES else None,
            # Adicione outros campos conforme necessário
        )
        new_donation.save()
        return redirect('minhas_doações')  # Redirecione conforme necessário
    return render(request, 'doar_item.html')

@login_required
def minhas_doacoes(request):
    doacoes = Doacao.objects.all()  # Recupera todas as doações
    return render(request, 'minhas_doacoes.html', {'doacoes': doacoes})

@login_required
def editar_doação(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id)

    if request.method == 'POST':
        doacao.item_name = request.POST.get('item_name')
        doacao.category = request.POST.get('category')
        doacao.condition = request.POST.get('condition')
        doacao.description = request.POST.get('description')
        
        if 'image' in request.FILES:
            doacao.image = request.FILES['image']
        
        doacao.save()
        return redirect('minhas_doações')

    return render(request, 'editar_doação.html', {'doacao': doacao})
    return render(request, 'editar_doação.html')

class LogoutWithGet(LogoutView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)