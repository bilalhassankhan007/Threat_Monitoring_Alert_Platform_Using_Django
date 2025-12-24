from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def home(request):
    # Renders the "all-in-one" local dashboard page
    return render(request, "monitoring/dashboard.html")


urlpatterns = [
    # ✅ Home dashboard
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    # App APIs
    path("api/", include("monitoring.urls")),
    # JWT Auth
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Swagger/OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
