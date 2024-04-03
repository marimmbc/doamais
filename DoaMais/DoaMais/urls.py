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
]