from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BannerViewSet

app_name = "banner"

router = DefaultRouter()
router.register(r"banners", BannerViewSet, basename="banner")

urlpatterns = [
    path("", include(router.urls)),
]
