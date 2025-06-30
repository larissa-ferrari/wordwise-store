from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Carrinho, ItemCarrinho
from .serializers import CarrinhoSerializer, AdicionarItemSerializer
from book.models import Livro
import uuid


class CarrinhoViewSet(GenericViewSet, RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = CarrinhoSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Carrinho.objects.none()

        request = self.request
        carrinho = None

        if request.user.is_authenticated:
            carrinho, _ = Carrinho.objects.get_or_create(
                cliente=request.user.cliente, status="ativo"
            )
        else:
            if not request.session.session_key:
                request.session.create()
                request.session["carrinho_id"] = str(uuid.uuid4())

            carrinho_id = request.session.get("carrinho_id")
            if carrinho_id:
                carrinho, _ = Carrinho.objects.get_or_create(
                    identificador=carrinho_id,
                    defaults={
                        "session_key": request.session.session_key,
                        "status": "ativo",
                    },
                )

        return (
            Carrinho.objects.filter(id=carrinho.id)
            if carrinho
            else Carrinho.objects.none()
        )

    def get_object(self):
        request = self.request
        carrinho = None

        if request.user.is_authenticated:
            carrinho, _ = Carrinho.objects.get_or_create(
                cliente=request.user.cliente, status="ativo"
            )
        else:
            if not request.session.session_key:
                request.session.create()
                request.session["carrinho_id"] = str(uuid.uuid4())

            carrinho_id = request.session.get("carrinho_id")
            if carrinho_id:
                carrinho, _ = Carrinho.objects.get_or_create(
                    identificador=carrinho_id,
                    defaults={
                        "session_key": request.session.session_key,
                        "status": "ativo",
                    },
                )
            else:
                request.session["carrinho_id"] = str(uuid.uuid4())
                carrinho = Carrinho.objects.create(
                    identificador=request.session["carrinho_id"],
                    session_key=request.session.session_key,
                    status="ativo",
                )

        return carrinho

    def adicionar_item(self, request):
        carrinho = self.get_object()
        serializer = AdicionarItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        livro = get_object_or_404(Livro, pk=serializer.validated_data["livro_id"])
        quantidade = serializer.validated_data["quantidade"]

        item, created = ItemCarrinho.objects.get_or_create(
            carrinho=carrinho, livro=livro, defaults={"quantidade": quantidade}
        )

        if not created:
            item.quantidade += quantidade
            item.save()

        return Response(self.get_serializer(carrinho).data, status=status.HTTP_200_OK)

    def remover_item(self, request, livro_id):
        carrinho = self.get_object()
        item = get_object_or_404(ItemCarrinho, carrinho=carrinho, livro_id=livro_id)
        item.delete()
        return Response(self.get_serializer(carrinho).data, status=status.HTTP_200_OK)
