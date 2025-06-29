from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Documentação da API do sistema",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("", include("user.urls")),
                path("", include("book.urls")),
                path("", include("category.urls")),
                path("", include("order.urls")),
                path("", include("support.urls")),
                path("", include("banner.urls")),
                path("cart/", include("cart.urls")),
            ]
        ),
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
]
