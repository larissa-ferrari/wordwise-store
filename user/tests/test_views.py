from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Cliente
from ..serializers import ClienteSerializer

User = get_user_model()


class ClienteViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="test123"
        )
        self.admin_user = User.objects.create_user(
            username="admin", email="admin@test.com", password="admin123", is_staff=True
        )
        self.cliente = Cliente.objects.create(
            user=self.user,
            nome="Test User",
            cpf="12345678901",
            telefone="11999999999",
            endereco="Rua Test, 123",
        )

    def test_create_cliente_without_auth(self):
        url = reverse("cliente-list")
        data = {
            "nome": "Novo Cliente",
            "email": "novo@test.com",
            "cpf": "98765432100",
            "telefone": "11888888888",
            "endereco": "Rua Nova, 456",
            "password": "nova123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_clientes_admin_only(self):
        url = reverse("cliente-list")

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(len(response.data["results"]), 1)  # Só vê o próprio

        # Admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_cliente_admin_only(self):
        """Apenas admin pode atualizar clientes"""
        url = reverse("cliente-detail", kwargs={"pk": self.cliente.pk})
        data = {"nome": "Nome Atualizado"}

        # Usuário comum
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
