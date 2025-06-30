from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, TransporteViewSet, MetodoPagamentoViewSet

app_name = "order"

router = DefaultRouter()
router.register(r"pedidos", PedidoViewSet, basename="pedido")
router.register(r"transportes", TransporteViewSet, basename="transporte")
router.register(r"pagamentos", MetodoPagamentoViewSet, basename="pagamento")

urlpatterns = [
    path("", include(router.urls)),
]
