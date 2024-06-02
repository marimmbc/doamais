# Importações Django para autenticação, visualizações e utilitários
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

# Importações de modelos específicos do seu aplicativo
from .models import Doacao, Avaliacao, User, SolicitacaoRecebida, Agendamento, Favorito


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
        user.location = request.POST.get('location')

        user.roupa = 'roupa' in request.POST
        user.eletronico = 'eletronico' in request.POST
        user.movel = 'movel' in request.POST
        user.livro = 'livro' in request.POST
        user.brinquedo = 'brinquedo' in request.POST

        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']

        user.save()
        return redirect('perfil')  # Certifique-se de que 'perfil' é o nome correto para a URL do perfil

    return render(request, 'editar_perfil.html', {'user': user})


@login_required
def pesquisar(request):
    resultados = None  # Começa sem nenhum resultado

    if request.method == 'GET':
        query = request.GET.get('title')
        category = request.GET.get('category')
        condition = request.GET.get('condition')

        if query or category or condition:  # Só faz a consulta se algum parâmetro de busca foi fornecido
            resultados = Doacao.objects.all()

            if query:
                resultados = resultados.filter(item_name__icontains=query)
            if category:
                resultados = resultados.filter(category=category)
            if condition:
                resultados = resultados.filter(condition=condition)

            # Verificar se cada item está marcado como favorito pelo usuário
            for item in resultados:
                item.is_favorite = Favorito.objects.filter(usuario=request.user, doacao=item).exists()

        return render(request, 'pesquisar.html', {'resultados': resultados})

    # Se não for GET, retorna erro
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)



@login_required
def itens_solicitados(request):
    solicitacoes = SolicitacaoRecebida.objects.select_related('doacao').all()
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
            donor=request.user
        )
        new_donation.save()
        return redirect('minhas_doacoes')  
    return render(request, 'doar_item.html')

@login_required
def minhas_doacoes(request):
    doacoes = Doacao.objects.filter(donor=request.user)
    print(doacoes)  # Isso irá mostrar no console os objetos de doações recuperados
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
    itens_favoritados_ids = request.user.favoritos.values_list('doacao_id', flat=True)
    return render(request, 'categoria_brinquedos.html', {
        'resultados': itens,
        'itens_favoritados_ids': list(itens_favoritados_ids)
    })

@login_required
def categoria_eletronicos(request):
    itens = Doacao.objects.filter(category='electronics')
    itens_favoritados_ids = request.user.favoritos.values_list('doacao_id', flat=True)
    return render(request, 'categoria_eletronicos.html', {
        'resultados': itens,
        'itens_favoritados_ids': list(itens_favoritados_ids)
    })

@login_required
def categoria_livros(request):
    itens = Doacao.objects.filter(category='book')
    itens_favoritados_ids = request.user.favoritos.values_list('doacao_id', flat=True)
    return render(request, 'categoria_livros.html', {
        'resultados': itens,
        'itens_favoritados_ids': list(itens_favoritados_ids)
    })

@login_required
def categoria_moveis(request):
    itens = Doacao.objects.filter(category='furniture')
    itens_favoritados_ids = request.user.favoritos.values_list('doacao_id', flat=True)
    return render(request, 'categoria_moveis.html', {
        'resultados': itens,
        'itens_favoritados_ids': list(itens_favoritados_ids)
    })

@login_required
def categoria_roupas(request):
    itens = Doacao.objects.filter(category='clothes')
    itens_favoritados_ids = request.user.favoritos.values_list('doacao_id', flat=True)
    return render(request, 'categoria_roupas.html', {
        'resultados': itens,
        'itens_favoritados_ids': list(itens_favoritados_ids)
    })


@login_required
def agendamento_view(request):
    if request.method == 'GET':
        doacoes = Doacao.objects.all()
        return render(request, 'agendamento.html', {'doacoes': doacoes})
    elif request.method == 'POST':
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
            return redirect('alguma_url_apos_sucesso')  # Altere 'alguma_url_apos_sucesso' para o nome real da URL de destino após o sucesso
        except Exception as e:
            messages.error(request, f'Erro ao criar agendamento: {e}')
            return redirect('agendamento')


@login_required 
def avaliacoes(request):
    doacoes_com_avaliacoes = Doacao.objects.filter(avaliacao__isnull=False).prefetch_related('avaliacao')
    doacoes_sem_avaliacoes = Doacao.objects.filter(avaliacao__isnull=True)
    return render(request, 'avaliacoes.html', {
        'doacoes_com_avaliacoes': doacoes_com_avaliacoes,
        'doacoes_sem_avaliacoes': doacoes_sem_avaliacoes,
        'range_1_to_6': range(1, 6)  # Adicionando o range ao contexto para uso no template
    })

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
    item = get_object_or_404(Doacao, pk=item_id)
    user_info = item.donor  # Supondo que donor seja a chave estrangeira para o usuário
    context = {
        'item': item,
        'user_info': user_info  # Passando informações do usuário para o template
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
    solicitacoes = SolicitacaoRecebida.objects.filter(doacao__donor=request.user, data_agendada__isnull=True)

    itens = []
    for solicitacao in solicitacoes:
        agendamento_info = None
        if solicitacao.data_agendada and solicitacao.hora_agendada:
            agendamento_info = f"{solicitacao.data_agendada} às {solicitacao.hora_agendada}"
        itens.append({
            'doacao': solicitacao.doacao,
            'show_agendamento_button': True,
            'agendamento_info': agendamento_info,
        })

    return render(request, 'solicitacoes_recebidas.html', {'itens': itens})

import json
@login_required
def favoritos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        item = get_object_or_404(Doacao, id=item_id)

        # Tentativa de obter um objeto Favorito existente
        favorito, created = Favorito.objects.get_or_create(usuario=request.user, doacao=item)
        if not created:  # Se o favorito já existe, ele deve ser excluído
            favorito.delete()
            favorited = False
        else:
            favorited = True  # Se foi criado, o item foi favoritado

        return JsonResponse({'favorited': favorited})
    else:
        # Para requisições GET, retornar a lista de favoritos
        favoritos = Favorito.objects.filter(usuario=request.user).select_related('doacao')
        return render(request, 'favoritos.html', {'favoritos': favoritos})



@login_required
def descricao_minhas_doacoes(request, item_id):
    item = get_object_or_404(Doacao, pk=item_id, donor=request.user)
    return render(request, 'descricao_minhas_doacoes.html', {'item': item})