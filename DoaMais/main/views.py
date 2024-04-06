from django.shortcuts import render, redirect, get_object_or_404
from .models import Doacao, SolicitarItem, User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LogoutView


def inicio(request):
    return render(request, 'inicio.html')

def cadastrar(request):
    if request.method == 'POST':
        # Your form processing logic...
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        photo = request.FILES.get('photo')

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            location=location,
            password=make_password(password)
        )

        if photo:
            user.photo = photo

        user.save()
        # Make sure 'some_success_url_name' is the name of the url you want to redirect to after a successful registration
        return redirect('pesquisar')  
    else:
        # GET request: just show the registration form.
        return render(request, 'cadastrar.html')  # Replace with your registration form template name

# No other return statement needed outside the if/else block.

   

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('pesquisar')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})

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