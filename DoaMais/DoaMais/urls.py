from django.urls import path
from main import views  

from django.contrib import admin


urlpatterns = [
    path('', views.login, name='login'),
    path('login', views.login, name='login'),
    path('cadastrar', views.cadastrar, name='cadastrar'),
    path('entrar', views.entrar, name='entrar'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('pesquisar/', views.pesquisar, name='pesquisar'),
    path('solicitar_item/', views.solicitar_item, name='solicitar_item'),
    path('itens_solicitados/', views.itens_solicitados, name='itens_solicitados'),
    path('doar_item/', views.doar_item, name='doar_item'),
    path('minhas_doações/', views.minhas_doações, name='minhas_doações'),
    path('editar_doação/<int:doacao_id>/', views.editar_doação, name='editar_doação'),
]