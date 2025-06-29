from .models import Categoria
from .serializers import CategoriaSerializer
from core.views import AuthenticatedModelViewSet

class CategoriaViewSet(AuthenticatedModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer