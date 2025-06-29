from django.urls import path
from .views_favoritos import FavoritoView
from .views_login import LoginView, LogoutView

urlpatterns = [
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("usuarios/favorites/<int:book_id>/", FavoritoView.as_view(), name="user-favorites"),
]
