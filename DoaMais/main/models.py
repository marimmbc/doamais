from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class SolicitarItem(models.Model):
    image = models.ImageField(upload_to='item_images/')
    title = models.CharField(max_length=255)
    CATEGORY_CHOICES = [
        ('clothes', 'Roupa'),
        ('furniture', 'Móvel'),
        ('electronics', 'Eletrônico'),
        ('toy', 'Brinquedo'),
        ('book', 'Livro'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    CONDITION_CHOICES = [
        ('new', 'Novo'),
        ('used_good', 'Usado - Bom'),
        ('used_acceptable', 'Usado - Aceitável'),
    ]
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.title    

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Doacao(models.Model):
    item_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='donations_images/', blank=True, null=True)
    CATEGORY_CHOICES = [
        ('clothes', 'Roupas'),
        ('furniture', 'Móveis'),
        ('electronics', 'Eletrônicos'),
        ('toys', 'Brinquedos'),
        ('books', 'Livros'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    CONDITION_CHOICES = [
        ('new', 'Novo'),
        ('used_good', 'Usado - Bom'),
        ('used_acceptable', 'Usado - Aceitável'),
    ]
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)

    def __str__(self):
        return f"{self.item_name} - {self.category}"
