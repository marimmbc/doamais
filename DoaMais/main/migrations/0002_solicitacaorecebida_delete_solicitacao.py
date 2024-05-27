# Generated by Django 5.0.3 on 2024-05-27 12:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacaoRecebida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_agendada', models.DateField(blank=True, null=True)),
                ('hora_agendada', models.TimeField(blank=True, null=True)),
                ('doacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes_recebidas', to='main.doacao')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes_recebidas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Solicitacao',
        ),
    ]
