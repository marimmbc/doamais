from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'  # O valor de 'name' deve ser o mesmo que o nome da pasta do aplicativo
