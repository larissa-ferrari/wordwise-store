from core.views import AuthenticatedModelViewSet
from .models import Suporte
from .serializers import SuporteSerializer

class SuporteViewSet(AuthenticatedModelViewSet):
    queryset = Suporte.objects.all()
    serializer_class = SuporteSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Suporte.objects.all()
        return Suporte.objects.filter(cliente=user.cliente)
