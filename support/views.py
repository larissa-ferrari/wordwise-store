from rest_framework.authentication import TokenAuthentication
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Suporte
from .serializers import SuporteSerializer

class SuporteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Suporte.objects.all()
    serializer_class = SuporteSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Suporte.objects.none()
        if user.is_staff:
            return Suporte.objects.all()
        return Suporte.objects.filter(cliente=user.cliente)
