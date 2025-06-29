from .models import User
from .serializers import UserSerializer
from core.views import AuthenticatedModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Cliente
from .serializers import ClienteSerializer, CriarClienteSerializer


class UserViewSet(AuthenticatedModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return CriarClienteSerializer
        return ClienteSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return []
        elif self.action in ["destroy", "update", "partial_update"]:
            return [IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)
