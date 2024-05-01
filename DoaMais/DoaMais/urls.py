from django.urls import path
from main import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login', views.login_view, name='login'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('solicitar_item/', views.solicitar_item, name='solicitar_item'),
    path('itens_solicitados/', views.itens_solicitados, name='itens_solicitados'),
    path('doar_item/', views.doar_item, name='doar_item'),
    path('minhas_doacoes/', views.minhas_doacoes, name='minhas_doacoes'),
    path('editar_doação/<int:doacao_id>/', views.editar_doação, name='editar_doação'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('categoria_brinquedos/', views.categoria_brinquedos, name='categoria_brinquedos'),
    path('categoria_eletronicos/', views.categoria_eletronicos, name='categoria_eletronicos'),
    path('categoria_livros/', views.categoria_livros, name='categoria_livros'),
    path('categoria_moveis/', views.categoria_moveis, name='categoria_moveis'),
    path('categoria_roupas/', views.categoria_roupas, name='categoria_roupas'),
    
]