from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class AuthenticatedModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base que exige autenticação para todas as operações.
    """
    permission_classes = [IsAuthenticated]
