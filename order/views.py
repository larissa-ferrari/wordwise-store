from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Pedido, Transporte, MetodoPagamento, ItemPedido
from cart.models import Carrinho
from .serializers import (
    MetodoPagamentoSerializer,
    PedidoSerializer,
    CriarPedidoSerializer,
    TransporteSerializer,
)


class PedidoViewSet(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin
):
    queryset = Pedido.objects.none()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.queryset

        if self.request.user.is_authenticated:
            return Pedido.objects.filter(cliente=self.request.user.cliente)
        return Pedido.objects.filter(session_key=self.request.session.session_key)

    def get_serializer_class(self):
        if self.action == "create":
            return CriarPedidoSerializer
        return PedidoSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transporte_id = serializer.validated_data["transporte"]
        metodo_pagamento_id = serializer.validated_data["metodo_pagamento"]
        endereco_entrega = serializer.validated_data["endereco_entrega"]
        observacoes = serializer.validated_data.get("observacoes", "")

        transporte = get_object_or_404(Transporte, id=transporte_id, ativo=True)
        metodo_pagamento = get_object_or_404(
            MetodoPagamento, id=metodo_pagamento_id, ativo=True
        )

        carrinho = self._obter_carrinho_ativo()

        if not carrinho:
            return Response(
                {"erro": "Nenhum carrinho ativo encontrado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        itens_carrinho = carrinho.itemcarrinho_set.all()
        if not itens_carrinho.exists():
            return Response(
                {"erro": "Carrinho está vazio"}, status=status.HTTP_400_BAD_REQUEST
            )

        pedido_data = {
            "transporte": transporte,
            "metodo_pagamento": metodo_pagamento,
            "endereco_entrega": endereco_entrega,
            "observacoes": observacoes,
        }

        if self.request.user.is_authenticated:
            pedido_data["cliente"] = self.request.user.cliente
        else:
            pedido_data["session_key"] = self.request.session.session_key

        pedido = Pedido.objects.create(**pedido_data)

        itens_pedido = []
        for item_carrinho in itens_carrinho:
            # Verificar estoque disponível
            if item_carrinho.livro.estoque < item_carrinho.quantidade:
                return Response(
                    {
                        "erro": f"Estoque insuficiente para o livro '{item_carrinho.livro.titulo}'. "
                        f"Disponível: {item_carrinho.livro.estoque}, Solicitado: {item_carrinho.quantidade}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item_pedido = ItemPedido(
                pedido=pedido,
                livro=item_carrinho.livro,
                quantidade=item_carrinho.quantidade,
                preco_unitario=item_carrinho.livro.preco,
            )
            itens_pedido.append(item_pedido)

        ItemPedido.objects.bulk_create(itens_pedido)

        for item_carrinho in itens_carrinho:
            item_carrinho.livro.estoque -= item_carrinho.quantidade
            item_carrinho.livro.save(update_fields=["estoque"])

        carrinho.status = "finalizado"
        carrinho.save()

        pedido_serializer = PedidoSerializer(pedido)
        return Response(pedido_serializer.data, status=status.HTTP_201_CREATED)

    def _obter_carrinho_ativo(self):
        try:
            if self.request.user.is_authenticated:
                return Carrinho.objects.get(
                    cliente=self.request.user.cliente, status="ativo"
                )
            else:
                session_key = self.request.session.session_key
                if not session_key:
                    self.request.session.create()
                    session_key = self.request.session.session_key

                return Carrinho.objects.get(session_key=session_key, status="ativo")
        except Carrinho.DoesNotExist:
            return None


class TransporteViewSet(GenericViewSet, ListModelMixin):
    queryset = Transporte.objects.filter(ativo=True)
    serializer_class = TransporteSerializer
    pagination_class = None


class MetodoPagamentoViewSet(GenericViewSet, ListModelMixin):
    queryset = MetodoPagamento.objects.filter(ativo=True)
    serializer_class = MetodoPagamentoSerializer
    pagination_class = None
