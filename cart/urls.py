from rest_framework.routers import DefaultRouter
from .views import CarrinhoViewSet

app_name = "cart"

router = DefaultRouter()
router.register(r"", CarrinhoViewSet, basename="carrinho")

urlpatterns = router.urls
