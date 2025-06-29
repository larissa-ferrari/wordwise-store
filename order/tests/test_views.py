from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Pedido, Transporte, MetodoPagamento, ItemPedido
from cart.models import Carrinho, ItemCarrinho
from book.models import Livro, Categoria
from user.models import User, Cliente


class PedidoViewSetTest(APITestCase):
    """Testes para PedidoViewSet"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test123")
        self.cliente = Cliente.objects.create(
            user=self.user, nome="Test User", cpf="12345678901"
        )

        self.categoria = Categoria.objects.create(nome="Teste")
        self.livro = Livro.objects.create(
            titulo="Livro Teste",
            autor="Autor",
            categoria=self.categoria,
            preco="29.90",
            estoque=10,
            status=True,
        )

        self.transporte = Transporte.objects.create(
            nome="Correios", preco="15.00", prazo_entrega=7, ativo=True
        )

        self.metodo_pagamento = MetodoPagamento.objects.create(
            nome="Cartão", ativo=True
        )

        # Criar carrinho com item
        self.carrinho = Carrinho.objects.create(cliente=self.cliente, status="ativo")
        ItemCarrinho.objects.create(
            carrinho=self.carrinho, livro=self.livro, quantidade=2
        )

    def test_create_pedido_success(self):
        """Criar pedido com sucesso"""
        self.client.force_authenticate(user=self.user)
        url = reverse("pedido-list")
        data = {
            "transporte": self.transporte.id,
            "metodo_pagamento": self.metodo_pagamento.id,
            "endereco_entrega": "Rua de Entrega, 123",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verificar se pedido foi criado
        pedido = Pedido.objects.get(cliente=self.cliente)
        self.assertEqual(pedido.itempedido_set.count(), 1)

        # Verificar se carrinho foi finalizado
        self.carrinho.refresh_from_db()
        self.assertEqual(self.carrinho.status, "finalizado")

        # Verificar se estoque foi atualizado
        self.livro.refresh_from_db()
        self.assertEqual(self.livro.estoque, 8)

    def test_create_pedido_insufficient_stock(self):
        """Criar pedido com estoque insuficiente"""
        # Reduzir estoque
        self.livro.estoque = 1
        self.livro.save()

        self.client.force_authenticate(user=self.user)
        url = reverse("pedido-list")
        data = {
            "transporte": self.transporte.id,
            "metodo_pagamento": self.metodo_pagamento.id,
            "endereco_entrega": "Rua de Entrega, 123",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Estoque insuficiente", response.data["erro"])

    def test_create_pedido_empty_cart(self):
        """Tentar criar pedido com carrinho vazio"""
        # Remover itens do carrinho
        self.carrinho.itemcarrinho_set.all().delete()

        self.client.force_authenticate(user=self.user)
        url = reverse("pedido-list")
        data = {
            "transporte": self.transporte.id,
            "metodo_pagamento": self.metodo_pagamento.id,
            "endereco_entrega": "Rua de Entrega, 123",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Carrinho está vazio", response.data["erro"])

    def test_list_pedidos_user_specific(self):
        """Usuário só vê seus próprios pedidos"""
        # Criar pedido
        pedido = Pedido.objects.create(
            cliente=self.cliente,
            transporte=self.transporte,
            metodo_pagamento=self.metodo_pagamento,
            endereco_entrega="Rua Test",
        )

        self.client.force_authenticate(user=self.user)
        url = reverse("pedido-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], pedido.id)
