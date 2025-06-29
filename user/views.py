from .models import User
from .serializers import UserSerializer
from core.views import AuthenticatedModelViewSet

class UserViewSet(AuthenticatedModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer