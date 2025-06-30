from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Pedido, Transporte, MetodoPagamento, ItemPedido
from cart.models import Carrinho
from .serializers import (
    MetodoPagamentoSerializer,
    PedidoSerializer,
    CriarPedidoSerializer,
    TransporteSerializer,
)
from rest_framework.pagination import PageNumberPagination


class PedidoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"


class PedidoViewSet(
    GenericViewSet, CreateModelMixin, RetrieveModelMixin, ListModelMixin
):
    permission_classes = [IsAuthenticated]
    queryset = Pedido.objects.none()
    pagination_class = PedidoPagination
    serializer_class = PedidoSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return self.queryset

        if self.request.user.is_authenticated:
            queryset = Pedido.objects.filter(cliente=self.request.user.cliente)
        else:
            queryset = Pedido.objects.filter(
                session_key=self.request.session.session_key
            )

        return queryset.order_by("-data_criacao")

    def get_serializer_class(self):
        if self.action == "create":
            return CriarPedidoSerializer
        return PedidoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transporte = serializer.validated_data["transporte_id"]
        metodo_pagamento = serializer.validated_data["metodo_pagamento_id"]
        endereco_entrega = serializer.validated_data["endereco_entrega"]
        observacoes = serializer.validated_data.get("observacoes", "")

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

        carrinho.status = "FINALIZADO"
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
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    queryset = Transporte.objects.filter(ativo=True)
    serializer_class = TransporteSerializer
    pagination_class = None


class MetodoPagamentoViewSet(GenericViewSet, ListModelMixin):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    queryset = MetodoPagamento.objects.filter(ativo=True)
    serializer_class = MetodoPagamentoSerializer
    pagination_class = None
