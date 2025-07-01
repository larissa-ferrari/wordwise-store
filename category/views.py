from .models import Categoria
from .serializers import CategoriaSerializer
from core.views import AuthenticatedModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated


class CategoriaViewSet(AuthenticatedModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
