from django.urls import path
from django.contrib.auth.views import LogoutView
from main import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login', views.login_view, name='login'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('itens_solicitados/', views.itens_solicitados, name='itens_solicitados'),
    path('doar_item/', views.doar_item, name='doar_item'),
    path('minhas_doacoes/', views.minhas_doacoes, name='minhas_doacoes'),
    path('editar_doação/<int:doacao_id>/', views.editar_doação, name='editar_doação'),
    path('logout/', views.LogoutWithGet.as_view(next_page='inicio'), name='logout'),
    path('categoria_brinquedos/', views.categoria_brinquedos, name='categoria_brinquedos'),
    path('categoria_eletronicos/', views.categoria_eletronicos, name='categoria_eletronicos'),
    path('categoria_livros/', views.categoria_livros, name='categoria_livros'),
    path('categoria_moveis/', views.categoria_moveis, name='categoria_moveis'),
    path('categoria_roupas/', views.categoria_roupas, name='categoria_roupas'),
    path('agendamento/', views.agendamento_view, name='agendamento'),
    path('avaliacoes/', views.avaliacoes, name='avaliacoes'),
    path('fazendo_avaliacao/<int:item_id>/', views.fazendo_avaliacao, name='fazendo_avaliacao'),
    path('descricao_item/<int:item_id>/', views.descricao_item, name='descricao_item'),
    path('solicitacoes_recebidas/', views.solicitacoes_recebidas, name='solicitacoes_recebidas'),
    path('favoritos/', views.favoritos, name='favoritos'),
]
