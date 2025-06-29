from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvaliacaoViewSet, ClienteFavoritosViewSet, LivroViewSet

app_name = "book"

router = DefaultRouter()
router.register(r"livros", LivroViewSet, basename="livro")
router.register(r"avaliacoes", AvaliacaoViewSet, basename="avaliacao")
router.register(r"favoritos", ClienteFavoritosViewSet, basename="favoritos")


urlpatterns = [
    path("", include(router.urls)),
]
