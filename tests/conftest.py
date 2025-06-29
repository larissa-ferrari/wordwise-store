import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from user.models import Cliente
from book.models import Livro, Categoria
from order.models import Transporte, MetodoPagamento

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser", email="test@test.com", password="test123"
    )


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username="admin",
        email="admin@test.com",
        password="admin123",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def cliente(user):
    return Cliente.objects.create(
        user=user,
        nome="Test User",
        cpf="12345678901",
        telefone="11999999999",
        endereco="Rua Test, 123",
    )


@pytest.fixture
def categoria():
    return Categoria.objects.create(nome="Ficção", descricao="Livros de ficção")


@pytest.fixture
def livro(categoria):
    return Livro.objects.create(
        titulo="Livro Teste",
        autor="Autor Teste",
        categoria=categoria,
        preco="29.90",
        estoque=10,
        descricao="Descrição teste",
        status=True,
    )


@pytest.fixture
def transporte():
    return Transporte.objects.create(
        nome="Correios PAC", preco="15.00", prazo_entrega=7, ativo=True
    )


@pytest.fixture
def metodo_pagamento():
    return MetodoPagamento.objects.create(
        nome="Cartão de Crédito", descricao="Pagamento via cartão", ativo=True
    )
