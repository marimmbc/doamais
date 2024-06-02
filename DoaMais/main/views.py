from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from .models import Doacao, Avaliacao, User, SolicitacaoRecebida, Agendamento, Favorito
from .models import UserProfile
import json

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
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    location=request.POST.get('location')
                )
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
    if request.method == 'POST':
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
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.userprofile.location = request.POST.get('location')

        if 'photo' in request.FILES:
            user.userprofile.photo = request.FILES['photo']

        user.save()
        user.userprofile.save()
        return redirect('perfil')

    return render(request, 'editar_perfil.html', {'user': user})



@login_required
def pesquisar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        item = get_object_or_404(Doacao, id=item_id)

        favorito, created = Favorito.objects.get_or_create(usuario=request.user, doacao=item)
        if not created:
            favorito.delete()
            favorited = False
        else:
            favorited = True

        return JsonResponse({'favorited': favorited})

    resultados = Doacao.objects.none()
    if request.method == 'GET':
        query = request.GET.get('title')
        category = request.GET.get('category')
        condition = request.GET.get('condition')

        if query or category or condition:
            resultados = Doacao.objects.filter(avaliacao__isnull=True)
            if query:
                resultados = resultados.filter(item_name__icontains=query)
            if category:
                resultados = resultados.filter(category=category)
            if condition:
                resultados = resultados.filter(condition=condition)

            for item in resultados:
                item.is_favorite = Favorito.objects.filter(usuario=request.user, doacao=item).exists()

    return render(request, 'pesquisar.html', {'resultados': resultados})


@login_required
def itens_solicitados(request):
    solicitacoes = SolicitacaoRecebida.objects.filter(solicitante=request.user).select_related('doacao', 'doacao__avaliacao').all()
    for solicitacao in solicitacoes:
        agendamentos = Agendamento.objects.filter(doacao=solicitacao.doacao).order_by('-data_agendamento', '-hora_agendamento')
        solicitacao.agendamento_recente = agendamentos.first() if agendamentos.exists() else None

    return render(request, 'itens_solicitados.html', {'solicitacoes': solicitacoes})

@login_required
def doar_item(request):
    if request.method == 'POST':
        new_donation = Doacao(
            item_name=request.POST.get('item_name'),
            category=request.POST.get('category'),
            condition=request.POST.get('condition'),
            image=request.FILES.get('image') if 'image' in request.FILES else None,
            donor=request.user,
            location=request.POST.get('location'),
            description=request.POST.get('description')
        )
        new_donation.save()
        return redirect('minhas_doacoes')
    return render(request, 'doar_item.html')

@login_required
def minhas_doacoes(request):
    doacoes = Doacao.objects.filter(donor=request.user, avaliacao__isnull=True)
    return render(request, 'minhas_doacoes.html', {'doacoes': doacoes})

@login_required
def editar_doacao(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            doacao.delete()
            return redirect('minhas_doacoes')
        
        doacao.item_name = request.POST.get('item_name')
        doacao.category = request.POST.get('category')
        doacao.condition = request.POST.get('condition')
        doacao.description = request.POST.get('description')
        
        if 'image' in request.FILES:
            doacao.image = request.FILES['image']
        
        doacao.save()
        return redirect('minhas_doacoes')

    return render(request, 'editar_doacao.html', {'doacao': doacao})

class LogoutWithGet(LogoutView):
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

@login_required
def categoria_brinquedos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        item = get_object_or_404(Doacao, id=item_id)

        favorito, created = Favorito.objects.get_or_create(usuario=request.user, doacao=item)
        if not created:
            favorito.delete()
            favorited = False
        else:
            favorited = True

        return JsonResponse({'favorited': favorited})

    itens = Doacao.objects.filter(category='toy', avaliacao__isnull=True).exclude(donor=request.user)
    for item in itens:
        item.is_favorite = Favorito.objects.filter(usuario=request.user, doacao=item).exists()

    return render(request, 'categoria_brinquedos.html', {'resultados': itens})

@login_required
def categoria_eletronicos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        item = get_object_or_404(Doacao, id=item_id)

        favorito, created = Favorito.objects.get_or_create(usuario=request.user, doacao=item)
        if not created:
            favorito.delete()
            favorited = False
        else:
            favorited = True

        return JsonResponse({'favorited': favorited})

    itens = Doacao.objects.filter(category='electronics', avaliacao__isnull=True).exclude(donor=request.user)
    for item in itens:
        item.is_favorite = Favorito.objects.filter(usuario=request.user, doacao=item).exists()

    return render(request, 'categoria_eletronicos.html', {'resultados': itens})

@login_required
def categoria_livros(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        item = get_object_or_404(Doacao, id=item_id)

        favorito, created = Favorito.objects.get_or_create(usuario=request.user, doacao=item)
        if not created:
            favorito.delete()
            favorited = False
        else:
            favorited = True

        return JsonResponse({'favorited': favorited})

    itens = Doacao.objects.filter(category='book', avaliacao__isnull=True).exclude(donor=request.user)
    for item in itens:
        item.is_favorite = Favorito.objects.filter(usuario=request.user, doacao=item).exists()

    return render(request, 'categoria_livros.html', {'resultados': itens})

@login_required
def categoria_moveis(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        item = get_object_or_404(Doacao, id=item_id)

        favorito, created = Favorito.objects.get_or_create(usuario=request.user, doacao=item)
        if not created:
            favorito.delete()
            favorited = False
        else:
            favorited = True

        return JsonResponse({'favorited': favorited})

    # Filtrar itens da categoria 'furniture' corretamente
    itens = Doacao.objects.filter(category='furniture', avaliacao__isnull=True).exclude(donor=request.user)
    for item in itens:
        item.is_favorite = Favorito.objects.filter(usuario=request.user, doacao=item).exists()

    return render(request, 'categoria_moveis.html', {'resultados': itens})



@login_required
def categoria_roupas(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        item = get_object_or_404(Doacao, id=item_id)

        favorito, created = Favorito.objects.get_or_create(usuario=request.user, doacao=item)
        if not created:
            favorito.delete()
            favorited = False
        else:
            favorited = True

        return JsonResponse({'favorited': favorited})

    itens = Doacao.objects.filter(category='clothes', avaliacao__isnull=True).exclude(donor=request.user)
    for item in itens:
        item.is_favorite = Favorito.objects.filter(usuario=request.user, doacao=item).exists()

    return render(request, 'categoria_roupas.html', {'resultados': itens})


@login_required
def agendamento_view(request, doacao_id):
    if request.method == 'GET':
        try:
            doacao = Doacao.objects.get(pk=doacao_id)
            return render(request, 'agendamento.html', {'doacoes': [doacao]})
        except Doacao.DoesNotExist:
            messages.error(request, "Doação não encontrada.")
            return redirect('agendamento')
    elif request.method == 'POST':
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
            return redirect('solicitacoes_recebidas')
        except Exception as e:
            messages.error(request, f'Erro ao criar agendamento: {e}')
            return redirect('agendamento')

@login_required 
def avaliacoes(request):
    doacoes_com_avaliacoes = Doacao.objects.filter(avaliacao__isnull=False).select_related('avaliacao')
    return render(request, 'avaliacoes.html', {
        'doacoes_com_avaliacoes': doacoes_com_avaliacoes,
        'range_1_to_6': range(1, 6)
    })

@login_required
def fazendo_avaliacao(request, item_id):
    doacao = get_object_or_404(Doacao, pk=item_id)
    if Avaliacao.objects.filter(doacao=doacao).exists():
        messages.info(request, 'Esta doação já foi avaliada.')
        return redirect('avaliacoes')

    stars_range = range(1, 6)

    if request.method == 'POST':
        avaliacao = Avaliacao(
            doacao=doacao,
            disponibilidade_entrega=request.POST.get('disponibilidade_entrega'),
            condicao_item=request.POST.get('condicao_item'),
            higiene_item=request.POST.get('higiene_item'),
            adequacao_descricao=request.POST.get('adequacao_descricao'),
            observacao=request.POST.get('observacao', '')
        )
        avaliacao.save()
        messages.success(request, 'Avaliação realizada com sucesso!')
        return redirect('avaliacoes')

    return render(request, 'fazendo_avaliacao.html', {'doacao': doacao, 'stars_range': stars_range})

@login_required
def descricao_item(request, item_id):
    item = get_object_or_404(Doacao, pk=item_id)
    user_info = item.donor
    context = {
        'item': item,
        'user_info': user_info
    }
    if request.method == 'POST':
        SolicitacaoRecebida.objects.create(doacao=item, solicitante=request.user)
        return redirect('itens_solicitados')
    return render(request, 'descricao_item.html', context)

@login_required
def excluir_doacao(request, doacao_id):
    doacao = get_object_or_404(Doacao, id=doacao_id)
    if request.method == 'POST':
        doacao.delete()
        return redirect('minhas_doacoes')
    return render(request, 'confirm_delete.html', {'doacao': doacao})

@login_required
def solicitacoes_recebidas(request):
    solicitacoes = SolicitacaoRecebida.objects.filter(doacao__donor=request.user)

    itens = []
    for solicitacao in solicitacoes:
        agendamento = Agendamento.objects.filter(doacao=solicitacao.doacao).first()
        if agendamento:
            show_agendamento_button = False
            agendamento_info = "Agendado"
        else:
            show_agendamento_button = True
            agendamento_info = None

        itens.append({
            'doacao': solicitacao.doacao,
            'show_agendamento_button': show_agendamento_button,
            'agendamento_info': agendamento_info,
        })

    return render(request, 'solicitacoes_recebidas.html', {'itens': itens})



@login_required
def favoritos(request):
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('doacao')
    return render(request, 'favoritos.html', {'favoritos': favoritos})

@login_required
def descricao_minhas_doacoes(request, item_id):
    item = get_object_or_404(Doacao, pk=item_id, donor=request.user)
    return render(request, 'descricao_minhas_doacoes.html', {'item': item})
