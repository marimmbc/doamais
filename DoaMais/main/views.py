from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Doacao, Avaliacao, SolicitarItem, User
from django.urls import reverse


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
       

        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']

        user.save()
        return redirect('perfil')  

    return render(request, 'editar_perfil.html', {'user': user})


@login_required
def pesquisar(request):
    query = request.GET.get('title')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    resultados = Doacao.objects.none()  # Inicia sem nenhum resultado

    # Verifica se todos os parâmetros foram fornecidos
    if query and category and condition:
        resultados = Doacao.objects.filter(item_name__icontains=query, category=category, condition=condition)

    return render(request, 'pesquisar.html', {'resultados': resultados})


@login_required
def itens_solicitados(request):
    itens = SolicitarItem.objects.all()
    for item in itens:
        agendamentos = Agendamento.objects.filter(doacao__solicitaritem=item).order_by('-data_agendamento', '-hora_agendamento')
        item.agendamento_recente = agendamentos.first() if agendamentos.exists() else None
    return render(request, 'itens_solicitados.html', {'itens': itens})

@login_required
def doar_item(request):
    if request.method == 'POST':
        new_donation = Doacao(
            item_name=request.POST.get('item_name'),
            category=request.POST.get('category'),
            condition=request.POST.get('condition'),
            image=request.FILES.get('image') if 'image' in request.FILES else None,
           
        )
        new_donation.save()
        return redirect('minhas_doacoes')  
    return render(request, 'doar_item.html')

@login_required
def minhas_doacoes(request):
    doacoes = Doacao.objects.all()
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


@login_required 
def categoria_brinquedos(request):
    itens = Doacao.objects.filter(category='toy')
    return render(request, 'categoria_brinquedos.html', {'resultados': itens})

@login_required 
def categoria_eletronicos(request):
    itens = Doacao.objects.filter(category='electronics')
    return render(request, 'categoria_eletronicos.html', {'resultados': itens})

@login_required 
def categoria_livros(request):
    itens = Doacao.objects.filter(category='book')
    return render(request, 'categoria_livros.html', {'resultados': itens})

@login_required 
def categoria_moveis(request):
    itens = Doacao.objects.filter(category='furniture')
    return render(request, 'categoria_moveis.html', {'resultados': itens})

@login_required 
def categoria_roupas(request):
    itens = Doacao.objects.filter(category='clothes')
    return render(request, 'categoria_roupas.html', {'resultados': itens})

from django.shortcuts import render, redirect
from django.views import View
from .models import Agendamento, Doacao
from django.contrib import messages

@login_required 
class AgendamentoView(View):
    template_name = 'agendamento.html'

    def get(self, request):
        doacoes = Doacao.objects.all()
        return render(request, self.template_name, {'doacoes': doacoes})

    def post(self, request):
        doacao_id = request.POST.get('doacao')
        data_agendamento = request.POST.get('data_agendamento')
        hora_agendamento = request.POST.get('hora_agendamento')

        try:
            doacao = Doacao.objects.get(pk=doacao_id)
            novo_agendamento = Agendamento(
                doacao=doacao,
                data_agendamento=data_agendamento,
                hora_agendamento=hora_agendamento
            )
            novo_agendamento.save()
            messages.success(request, 'Agendamento criado com sucesso!')
            return redirect('alguma_url_apos_sucesso')
        except Exception as e:
            messages.error(request, f'Erro ao criar agendamento: {e}')
            return redirect('agendamento')


from django.shortcuts import render
from .models import Doacao

@login_required 
def avaliacoes(request):
    doacoes_com_avaliacoes = Doacao.objects.filter(avaliacao__isnull=False).prefetch_related('avaliacao')
    doacoes_sem_avaliacoes = Doacao.objects.filter(avaliacao__isnull=True)
    return render(request, 'avaliacoes.html', {
        'doacoes_com_avaliacoes': doacoes_com_avaliacoes,
        'doacoes_sem_avaliacoes': doacoes_sem_avaliacoes
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doacao, Avaliacao

@login_required
def fazendo_avaliacao(request, item_id):  # Usando item_id conforme sua URL
    doacao = get_object_or_404(Doacao, pk=item_id)  # Usa item_id para buscar a doação

    # Verifica se a doação já foi avaliada
    try:
        avaliacao = Avaliacao.objects.get(doacao=doacao)
        messages.info(request, 'Esta doação já foi avaliada.')
        return redirect('avaliacoes')  # Redireciona para a lista de avaliações
    except Avaliacao.DoesNotExist:
        # Se não foi avaliada, continua para a página de avaliação
        pass

    if request.method == 'POST':
        avaliacao = Avaliacao(
            doacao=doacao,
            disponibilidade_entrega=request.POST['disponibilidade_entrega'],
            condicao_item=request.POST['condicao_item'],
            higiene_item=request.POST['higiene_item'],
            adequacao_descricao=request.POST['adequacao_descricao'],
            observacao=request.POST.get('observacao', '')
        )
        avaliacao.save()
        messages.success(request, 'Avaliação realizada com sucesso!')
        return redirect('avaliacoes')  # Redireciona para a lista de avaliações após sucesso

    return render(request, 'fazendo_avaliacao.html', {'doacao': doacao})

@login_required
def descricao_item(request, item_id):
    # Busca o item específico pelo ID, usando get_object_or_404 para retornar um erro 404 se o item não existir
    item = get_object_or_404(Doacao, pk=item_id)
    
    # Renderiza o template descricao_item.html, passando o item buscado como contexto
    return render(request, 'descricao_item.html', {'item': item})

@login_required
def excluir_doacao(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id)
    if request.method == 'POST':
        doacao.delete()
        return redirect('minhas_doacoes')
    return render(request, 'confirm_delete.html', {'doacao': doacao})