from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions


api_info = openapi.Info(title="Documentation", default_version="v1")

class HttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
    api_info,
    public=True,
    generator_class=HttpAndHttpsSchemaGenerator,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
         "api/",
        include(
            [
                path("", include("users.urls", namespace="users")),
                path("organisations/", include("organisations.urls", namespace="organisations")),
            ]
        ),
    ),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r"^doc/", schema_view.with_ui("swagger")),
    re_path(r"^redoc/", schema_view.with_ui("redoc")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)