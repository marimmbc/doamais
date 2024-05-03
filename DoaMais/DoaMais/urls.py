from django.urls import path
from django.contrib.auth.views import LogoutView
from main.views import (
    inicio, login_view, cadastrar, perfil, editar_perfil, pesquisar,
    solicitar_item, itens_solicitados, doar_item, minhas_doacoes,
    editar_doação, categoria_brinquedos, categoria_eletronicos,
    categoria_livros, categoria_moveis, categoria_roupas, avaliacoes,
    fazendo_avaliacao, LogoutWithGet, AgendamentoView, descricao_item)

urlpatterns = [
    path('', inicio, name='inicio'),
    path('login', login_view, name='login'),
    path('cadastrar', cadastrar, name='cadastrar'),
    path('perfil/', perfil, name='perfil'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('pesquisar/', pesquisar, name='pesquisar'),
    path('solicitar_item/', solicitar_item, name='solicitar_item'),
    path('itens_solicitados/', itens_solicitados, name='itens_solicitados'),
    path('doar_item/', doar_item, name='doar_item'),
    path('minhas_doacoes/', minhas_doacoes, name='minhas_doacoes'),
    path('editar_doação/<int:doacao_id>/', editar_doação, name='editar_doação'),
    path('logout/', LogoutWithGet.as_view(next_page='inicio'), name='logout'),
    path('categoria_brinquedos/', categoria_brinquedos, name='categoria_brinquedos'),
    path('categoria_eletronicos/', categoria_eletronicos, name='categoria_eletronicos'),
    path('categoria_livros/', categoria_livros, name='categoria_livros'),
    path('categoria_moveis/', categoria_moveis, name='categoria_moveis'),
    path('categoria_roupas/', categoria_roupas, name='categoria_roupas'),
    path('agendamento/', AgendamentoView.as_view(), name='agendamento'),
    path('avaliacoes/', avaliacoes, name='avaliacoes'),
    path('fazendo_avaliacao/<int:item_id>/', fazendo_avaliacao, name='fazendo_avaliacao'),
    path('descricao_item/<int:item_id>/', descricao_item, name='descricao_item'),
]
