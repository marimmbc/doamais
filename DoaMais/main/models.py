from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    def __str__(self):
        return self.user.username
    
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, first_name=None, last_name=None, location=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            location=location,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class Doacao(models.Model):

    CATEGORY_CHOICES = [
        ('clothes', 'Roupa'),
        ('furniture', 'Móvel'),
        ('electronics', 'Eletrônico'),
        ('toy', 'Brinquedo'),
        ('book', 'Livro'),
    ]
    CONDITION_CHOICES = [
        ('new', 'Novo'),
        ('used_good', 'Usado - Bom'),
        ('used_acceptable', 'Usado - Aceitável'),
    ]

    item_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='donations_images/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doacoes')
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item_name} - {self.category}"

class Agendamento(models.Model):
    doacao = models.ForeignKey(Doacao, on_delete=models.CASCADE, verbose_name="Doação Relacionada")
    data_agendamento = models.DateField(verbose_name="Data do Agendamento")
    hora_agendamento = models.TimeField(verbose_name="Hora do Agendamento")

    def __str__(self):
        return f"Agendamento para {self.doacao.item_name} em {self.data_agendamento} às {self.hora_agendamento}"
    
    
class Avaliacao(models.Model):
    doacao = models.OneToOneField(Doacao, on_delete=models.CASCADE, related_name='avaliacao')
    disponibilidade_entrega = models.IntegerField(verbose_name="Disponibilidade de Entrega/Retirada", choices=[(i, f'{i} Estrelas') for i in range(1, 6)])
    condicao_item = models.IntegerField(verbose_name="Condição do Item", choices=[(i, f'{i} Estrelas') for i in range(1, 6)])
    higiene_item = models.IntegerField(verbose_name="Higiene do Item", choices=[(i, f'{i} Estrelas') for i in range(1, 6)])
    adequacao_descricao = models.IntegerField(verbose_name="Adequação à Descrição", choices=[(i, f'{i} Estrelas') for i in range(1, 6)])
    observacao = models.TextField(verbose_name="Observação", blank=True, null=True)

    def average_stars(self):
        total = (self.disponibilidade_entrega + self.condicao_item + self.higiene_item + self.adequacao_descricao)
        return total / 4.0

    def __str__(self):
        return f"Avaliação #{self.id} - {self.condicao_item} estrelas para condição do item"

class SolicitacaoRecebida(models.Model):
    doacao = models.ForeignKey(Doacao, on_delete=models.CASCADE, related_name='solicitacoes_recebidas')
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitacoes_recebidas')
    data_agendada = models.DateField(blank=True, null=True)
    hora_agendada = models.TimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.solicitante.username} - {self.doacao.item_name}"


class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos')
    doacao = models.ForeignKey('Doacao', on_delete=models.CASCADE, related_name='marcados_como_favorito')

    def __str__(self):
        return f'{self.usuario.username} favoritou {self.doacao.item_name}'

