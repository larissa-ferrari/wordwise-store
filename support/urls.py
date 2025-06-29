from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuporteViewSet

app_name = "support"

router = DefaultRouter()
router.register(r"suportes", SuporteViewSet, basename="suporte")

urlpatterns = [
    path("", include(router.urls)),
]
