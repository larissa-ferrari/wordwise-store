from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet
from .views_favoritos import FavoritoView
from .views_login import LoginView, LogoutView

app_name = "user"

router = DefaultRouter()
router.register(r"clientes", ClienteViewSet, basename="clientes")

urlpatterns = [
    path("clientes/login/", LoginView.as_view(), name="login"),
    path("clientes/logout/", LogoutView.as_view(), name="logout"),
    path(
        "clientes/favorites/<int:book_id>/",
        FavoritoView.as_view(),
        name="user-favorites",
    ),
] + router.urls
