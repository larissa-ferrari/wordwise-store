from core.views import AuthenticatedModelViewSet
from .models import Banner
from .serializers import BannerSerializer

class BannerViewSet(AuthenticatedModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
