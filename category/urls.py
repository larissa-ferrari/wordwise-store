from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet

app_name = "category"

router = DefaultRouter()
router.register(r"categorias", CategoriaViewSet, basename="categoria")

urlpatterns = [
    path("", include(router.urls)),
]
