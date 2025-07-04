# Generated by Django 5.2.3 on 2025-06-29 22:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('dt_criacao', models.DateTimeField(auto_now_add=True)),
                ('dt_atualizacao', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='ativo', max_length=50)),
                ('identificador', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
            ],
        ),
    ]
