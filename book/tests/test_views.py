from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import Livro, Categoria, Avaliacao
from user.models import User, Cliente


class LivroViewSetTest(APITestCase):
    """Testes para LivroViewSet"""

    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome="Ficção", descricao="Livros de ficção"
        )
        self.livro = Livro.objects.create(
            titulo="Livro Teste",
            autor="Autor Teste",
            categoria=self.categoria,
            preco="29.90",
            estoque=10,
            descricao="Descrição teste",
            status=True,
        )
        self.user = User.objects.create_user(username="testuser", password="test123")
        self.cliente = Cliente.objects.create(
            user=self.user, nome="Test User", cpf="12345678901"
        )

    def test_list_livros_public(self):
        """Listagem de livros é pública"""
        url = reverse("livro-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_search_livros_by_titulo(self):
        """Buscar livros por título"""
        url = reverse("livro-search")
        response = self.client.get(url, {"titulo": "Teste"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["titulo"], "Livro Teste")

    def test_search_livros_by_price_range(self):
        """Buscar livros por faixa de preço"""
        url = reverse("livro-search")
        response = self.client.get(url, {"preco_min": "20", "preco_max": "40"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_avaliacao_authenticated(self):
        """Criar avaliação requer autenticação"""
        self.client.force_authenticate(user=self.user)
        url = reverse("avaliacao-list")
        data = {"livro_id": self.livro.id, "nota": 5, "comentario": "Excelente!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_avaliacoes_livro(self):
        """Listar avaliações de um livro"""
        # Criar avaliação primeiro
        Avaliacao.objects.create(
            livro=self.livro, cliente=self.cliente, nota=4, comentario="Bom livro"
        )

        url = reverse("livro-avaliacoes", kwargs={"pk": self.livro.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
