import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
import uuid

# Assumindo que os modelos estão nos seguintes apps
from user.models import Endereco, User, Cliente
from book.models import Livro, Categoria, Avaliacao, ClienteFavoritos
from cart.models import Carrinho, ItemCarrinho
from order.models import Pedido, ItemPedido, Transporte, MetodoPagamento


class EcommerceFlowTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Criar usuários
        self.user_admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            is_staff=True,
            is_superuser=True,
        )

        self.user_cliente = User.objects.create_user(
            username="cliente1",
            email="cliente1@test.com",
            password="cliente123",
            first_name="João",
            last_name="Silva",
            phone="11999999999",  # campo correto no seu AbstractUser
        )

        self.cliente = Cliente.objects.create(
            user=self.user_cliente,
            cpf="12345678901",
        )

        self.endereco = Endereco.objects.create(
            cliente=self.cliente,
            rua="Rua Test",
            numero="123",
            complemento="",
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            cep="01000-000",
            pais="Brasil",
            principal=True,
        )

        # Criar categoria
        self.categoria = Categoria.objects.create(
            nome="Ficção Científica", descricao="Livros de ficção científica"
        )

        # Criar livros
        self.livro1 = Livro.objects.create(
            titulo="1984",
            autor="George Orwell",
            categoria=self.categoria,
            preco=Decimal("29.90"),
            estoque=10,
            descricao="Romance distópico",
            status=True,
            ano_publicacao=2000,
            numero_paginas=20,
        )

        self.livro2 = Livro.objects.create(
            titulo="Duna",
            autor="Frank Herbert",
            categoria=self.categoria,
            preco=Decimal("45.00"),
            estoque=5,
            descricao="Épico de ficção científica",
            status=True,
            ano_publicacao=1999,
            numero_paginas=10,
        )

        # Criar transporte e método de pagamento
        self.transporte = Transporte.objects.create(
            nome="Correios PAC",
            valor=Decimal("15.00"),
            prazo_dias=7,
            ativo=True,
        )

        self.metodo_pagamento = MetodoPagamento.objects.create(
            nome="Cartão de Crédito",
            ativo=True,
        )

    def test_01_criar_cliente_sem_autenticacao(self):
        data = {
            "user": {
                "username": "marias",
                "first_name": "Maria",
                "last_name": "Santos",
                "email": "maria@test.com",
                "phone": "11888888888",
            },
            "password": "maria123",
            "cpf": "40647955806",
        }

        url = reverse("user:clientes-list")
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Cliente.objects.filter(cpf="40647955806").exists())

    def test_02_listar_livros_sem_autenticacao(self):
        url = reverse("book:livro-list")
        response = self.client.get(url)

        print(response.status_code)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    # def test_03_buscar_livros(self):
    #     """Teste: Buscar livros por título e autor"""
    #     url = reverse("livro-search")

    #     # Buscar por título
    #     response = self.client.get(url, {"titulo": "1984"})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]["titulo"], "1984")

    #     # Buscar por autor
    #     response = self.client.get(url, {"autor": "Frank"})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]["autor"], "Frank Herbert")

    #     # Buscar por faixa de preço
    #     response = self.client.get(url, {"preco_min": "30", "preco_max": "50"})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]["titulo"], "Duna")

    # def test_04_carrinho_usuario_nao_autenticado(self):
    #     """Teste: Funcionalidades do carrinho para usuário não autenticado"""
    #     # Obter carrinho (deve criar um novo)
    #     url = reverse("carrinho-detail", kwargs={"pk": 1})
    #     response = self.client.get(url)

    #     # Como não existe carrinho com ID 1, deve retornar o carrinho criado automaticamente
    #     self.assertTrue(
    #         response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
    #     )

    #     # Adicionar item ao carrinho
    #     url = reverse("carrinho-adicionar-item")
    #     data = {"livro_id": self.livro1.id, "quantidade": 2}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Verificar se o item foi adicionado
    #     self.assertTrue("itens" in response.data)

    # def test_05_autenticacao_e_carrinho_usuario_logado(self):
    #     """Teste: Carrinho para usuário autenticado"""
    #     # Fazer login
    #     self.client.force_authenticate(user=self.user_cliente)

    #     # Adicionar item ao carrinho
    #     url = reverse("carrinho-adicionar-item")
    #     data = {"livro_id": self.livro1.id, "quantidade": 1}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Adicionar outro item
    #     data = {"livro_id": self.livro2.id, "quantidade": 2}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Verificar carrinho
    #     carrinho = Carrinho.objects.get(cliente=self.cliente, status="ativo")
    #     self.assertEqual(carrinho.itemcarrinho_set.count(), 2)

    #     # Remover item do carrinho
    #     url = reverse("carrinho-remover-item", kwargs={"livro_id": self.livro1.id})
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Verificar se item foi removido
    #     carrinho.refresh_from_db()
    #     self.assertEqual(carrinho.itemcarrinho_set.count(), 1)

    # def test_06_adicionar_favoritos(self):
    #     """Teste: Adicionar e remover favoritos"""
    #     self.client.force_authenticate(user=self.user_cliente)

    #     # Adicionar aos favoritos
    #     url = reverse("clientefavoritos-toggle", kwargs={"pk": self.livro1.id})
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data["status"], "added")

    #     # Verificar se foi adicionado
    #     self.assertTrue(
    #         ClienteFavoritos.objects.filter(
    #             cliente=self.cliente, livro=self.livro1
    #         ).exists()
    #     )

    #     # Remover dos favoritos
    #     response = self.client.post(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["status"], "removed")

    #     # Verificar se foi removido
    #     self.assertFalse(
    #         ClienteFavoritos.objects.filter(
    #             cliente=self.cliente, livro=self.livro1
    #         ).exists()
    #     )

    # def test_07_criar_avaliacao(self):
    #     """Teste: Criar avaliação para um livro"""
    #     self.client.force_authenticate(user=self.user_cliente)

    #     url = reverse("avaliacao-list")
    #     data = {"livro_id": self.livro1.id, "nota": 5, "comentario": "Excelente livro!"}

    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # Verificar se a avaliação foi criada
    #     avaliacao = Avaliacao.objects.get(livro=self.livro1, cliente=self.cliente)
    #     self.assertEqual(avaliacao.nota, 5)
    #     self.assertEqual(avaliacao.comentario, "Excelente livro!")

    #     # Listar avaliações do livro
    #     url = reverse("livro-avaliacoes", kwargs={"pk": self.livro1.id})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)

    # def test_08_criar_pedido_completo(self):
    #     """Teste: Fluxo completo de criação de pedido"""
    #     self.client.force_authenticate(user=self.user_cliente)

    #     # 1. Adicionar itens ao carrinho
    #     url = reverse("carrinho-adicionar-item")

    #     # Adicionar livro 1
    #     data = {"livro_id": self.livro1.id, "quantidade": 2}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Adicionar livro 2
    #     data = {"livro_id": self.livro2.id, "quantidade": 1}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # 2. Verificar estoque antes do pedido
    #     estoque_inicial_livro1 = self.livro1.estoque
    #     estoque_inicial_livro2 = self.livro2.estoque

    #     # 3. Criar pedido
    #     url = reverse("pedido-list")
    #     data = {
    #         "transporte": self.transporte.id,
    #         "metodo_pagamento": self.metodo_pagamento.id,
    #         "endereco_entrega": "Rua de Entrega, 789",
    #         "observacoes": "Entregar no período da manhã",
    #     }

    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # 4. Verificar se o pedido foi criado corretamente
    #     pedido = Pedido.objects.get(cliente=self.cliente)
    #     self.assertEqual(pedido.status, "pendente")  # assumindo status padrão
    #     self.assertEqual(pedido.itempedido_set.count(), 2)

    #     # 5. Verificar se o estoque foi atualizado
    #     self.livro1.refresh_from_db()
    #     self.livro2.refresh_from_db()
    #     self.assertEqual(self.livro1.estoque, estoque_inicial_livro1 - 2)
    #     self.assertEqual(self.livro2.estoque, estoque_inicial_livro2 - 1)

    #     # 6. Verificar se o carrinho foi finalizado
    #     carrinho = Carrinho.objects.get(cliente=self.cliente)
    #     self.assertEqual(carrinho.status, "finalizado")

    # def test_09_pedido_estoque_insuficiente(self):
    #     """Teste: Tentar criar pedido com estoque insuficiente"""
    #     self.client.force_authenticate(user=self.user_cliente)

    #     # Reduzir estoque do livro2 para 1
    #     self.livro2.estoque = 1
    #     self.livro2.save()

    #     # Adicionar mais itens do que o estoque disponível
    #     url = reverse("carrinho-adicionar-item")
    #     data = {"livro_id": self.livro2.id, "quantidade": 3}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Tentar criar pedido
    #     url = reverse("pedido-list")
    #     data = {
    #         "transporte": self.transporte.id,
    #         "metodo_pagamento": self.metodo_pagamento.id,
    #         "endereco_entrega": "Rua de Entrega, 789",
    #     }

    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("Estoque insuficiente", response.data["erro"])

    # def test_10_listar_pedidos_cliente(self):
    #     """Teste: Listar pedidos do cliente"""
    #     self.client.force_authenticate(user=self.user_cliente)

    #     # Primeiro criar um pedido (reutilizando lógica do teste anterior)
    #     # Adicionar item ao carrinho
    #     url = reverse("carrinho-adicionar-item")
    #     data = {"livro_id": self.livro1.id, "quantidade": 1}
    #     self.client.post(url, data)

    #     # Criar pedido
    #     url = reverse("pedido-list")
    #     data = {
    #         "transporte": self.transporte.id,
    #         "metodo_pagamento": self.metodo_pagamento.id,
    #         "endereco_entrega": "Rua de Entrega, 789",
    #     }
    #     self.client.post(url, data)

    #     # Listar pedidos
    #     url = reverse("pedido-list")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data["results"]), 1)

    # def test_11_permissoes_admin(self):
    #     """Teste: Funcionalidades administrativas"""
    #     # Testar como usuário comum
    #     self.client.force_authenticate(user=self.user_cliente)

    #     # Tentar criar livro (deve falhar)
    #     url = reverse("livro-list")
    #     data = {
    #         "titulo": "Novo Livro",
    #         "autor": "Autor Teste",
    #         "categoria": self.categoria.id,
    #         "preco": "25.00",
    #         "estoque": 5,
    #         "descricao": "Descrição teste",
    #     }
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #     # Testar como admin
    #     self.client.force_authenticate(user=self.user_admin)

    #     # Criar livro (deve funcionar)
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # Atualizar cliente (deve funcionar para admin)
    #     cliente_url = reverse("cliente-detail", kwargs={"pk": self.cliente.id})
    #     data = {"nome": "João Silva Atualizado"}
    #     response = self.client.patch(cliente_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_12_listar_opcoes_transporte_pagamento(self):
    #     """Teste: Listar opções de transporte e pagamento"""
    #     # Listar transportes
    #     url = reverse("transporte-list")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]["nome"], "Correios PAC")

    #     # Listar métodos de pagamento
    #     url = reverse("metodopagamento-list")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]["nome"], "Cartão de Crédito")
