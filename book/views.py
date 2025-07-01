from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Livro, Avaliacao, ClienteFavoritos
from .serializers import (
    LivroSerializer,
    AvaliacaoSerializer,
    ClienteFavoritosSerializer,
)
from user.models import Cliente
from django.shortcuts import get_object_or_404
from core.views import AuthenticatedModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg
import random
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet, filters
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins, viewsets


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class LivroFilter(FilterSet):
    categoria = filters.CharFilter(field_name="categoria__nome", lookup_expr="iexact")
    autor = filters.CharFilter(field_name="autor", lookup_expr="icontains")
    tipo = filters.CharFilter(field_name="tipo", lookup_expr="icontains")

    class Meta:
        model = Livro
        fields = ["autor", "categoria", "tipo"]


class LivroViewSet(AuthenticatedModelViewSet):
    queryset = Livro.objects.filter(status=True)
    serializer_class = LivroSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = LivroFilter

    def get_permissions(self):
        if self.action in ["list", "retrieve", "search", "avaliacoes", "destaques"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_destroy(self, instance):
        instance.status = False
        instance.save()

    @action(detail=False, methods=["get"])
    def search(self, request):
        queryset = self.get_queryset()

        titulo = request.query_params.get("titulo", None)
        autor = request.query_params.get("autor", None)
        categoria = request.query_params.get("categoria", None)
        preco_min = request.query_params.get("preco_min", None)
        preco_max = request.query_params.get("preco_max", None)

        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
        if autor:
            queryset = queryset.filter(autor__icontains=autor)
        if categoria:
            queryset = queryset.filter(categoria__id=categoria)
        if preco_min:
            queryset = queryset.filter(preco__gte=float(preco_min))
        if preco_max:
            queryset = queryset.filter(preco__lte=float(preco_max))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def avaliacoes(self, request, pk=None):
        livro = self.get_object()
        avaliacoes = Avaliacao.objects.filter(livro=livro)
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="destaques")
    def destaques(self, request):
        livros_avaliados = (
            self.get_queryset()
            .annotate(media=Avg("avaliacao__nota"))
            .order_by("-media")
        )

        livros_destacados = list(livros_avaliados[:4])

        if len(livros_destacados) < 4:
            faltando = 4 - len(livros_destacados)
            outros = self.get_queryset().exclude(
                id__in=[l.id for l in livros_destacados]
            )
            outros_aleatorios = random.sample(
                list(outros), min(faltando, outros.count())
            )
            livros_destacados.extend(outros_aleatorios)

        serializer = self.get_serializer(livros_destacados, many=True)
        return Response(serializer.data)


class AvaliacaoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        livro = get_object_or_404(Livro, pk=self.request.data.get("livro_id"))
        cliente = get_object_or_404(Cliente, user=self.request.user)
        serializer.save(livro=livro, cliente=cliente)


class ClienteFavoritosViewSet(AuthenticatedModelViewSet):
    serializer_class = ClienteFavoritosSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return ClienteFavoritos.objects.none()

        try:
            cliente = Cliente.objects.get(user=self.request.user)
            return ClienteFavoritos.objects.filter(cliente=cliente)
        except Cliente.DoesNotExist:
            return ClienteFavoritos.objects.none()

    @action(detail=True, methods=["post"])
    def toggle(self, request, pk=None):
        cliente = get_object_or_404(Cliente, user=request.user)
        livro = get_object_or_404(Livro, pk=pk)

        favorito, created = ClienteFavoritos.objects.get_or_create(
            cliente=cliente, livro=livro
        )

        if not created:
            favorito.delete()
            return Response({"status": "removed"}, status=status.HTTP_200_OK)

        return Response({"status": "added"}, status=status.HTTP_201_CREATED)
