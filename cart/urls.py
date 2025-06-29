from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CarrinhoViewSet

app_name = "cart"

router = DefaultRouter()
router.register(r"carrinho", CarrinhoViewSet, basename="carrinho")

urlpatterns = [
    path(
        "adicionar/",
        CarrinhoViewSet.as_view({"post": "adicionar_item"}),
        name="adicionar-item",
    ),
    path(
        "remover/<int:livro_id>/",
        CarrinhoViewSet.as_view({"delete": "remover_item"}),
        name="remover-item",
    ),
] + router.urls
