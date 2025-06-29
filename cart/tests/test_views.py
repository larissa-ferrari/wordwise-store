from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Carrinho, ItemCarrinho
from book.models import Livro, Categoria
from user.models import User, Cliente


class CarrinhoViewSetTest(APITestCase):
    """Testes para CarrinhoViewSet"""

    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Teste")
        self.livro = Livro.objects.create(
            titulo="Livro Teste",
            autor="Autor",
            categoria=self.categoria,
            preco="29.90",
            estoque=10,
            status=True,
        )
        self.user = User.objects.create_user(username="testuser", password="test123")
        self.cliente = Cliente.objects.create(
            user=self.user, nome="Test User", cpf="12345678901"
        )

    def test_add_item_anonymous_user(self):
        """Usuário anônimo pode adicionar itens ao carrinho"""
        url = reverse("carrinho-adicionar-item")
        data = {"livro_id": self.livro.id, "quantidade": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("itens", response.data)

    def test_add_item_authenticated_user(self):
        """Usuário autenticado pode adicionar itens ao carrinho"""
        self.client.force_authenticate(user=self.user)
        url = reverse("carrinho-adicionar-item")
        data = {"livro_id": self.livro.id, "quantidade": 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar se carrinho foi criado para o cliente
        carrinho = Carrinho.objects.get(cliente=self.cliente, status="ativo")
        self.assertEqual(carrinho.itemcarrinho_set.count(), 1)

    def test_add_same_item_increases_quantity(self):
        """Adicionar o mesmo item aumenta a quantidade"""
        self.client.force_authenticate(user=self.user)
        url = reverse("carrinho-adicionar-item")
        data = {"livro_id": self.livro.id, "quantidade": 2}

        # Primeira adição
        self.client.post(url, data)

        # Segunda adição
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar quantidade
        carrinho = Carrinho.objects.get(cliente=self.cliente, status="ativo")
        item = carrinho.itemcarrinho_set.first()
        self.assertEqual(item.quantidade, 4)

    def test_remove_item_from_cart(self):
        """Remover item do carrinho"""
        self.client.force_authenticate(user=self.user)

        # Adicionar item primeiro
        carrinho, _ = Carrinho.objects.get_or_create(
            cliente=self.cliente, status="ativo"
        )
        ItemCarrinho.objects.create(carrinho=carrinho, livro=self.livro, quantidade=2)

        # Remover item
        url = reverse("carrinho-remover-item", kwargs={"livro_id": self.livro.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar se foi removido
        self.assertEqual(carrinho.itemcarrinho_set.count(), 0)
