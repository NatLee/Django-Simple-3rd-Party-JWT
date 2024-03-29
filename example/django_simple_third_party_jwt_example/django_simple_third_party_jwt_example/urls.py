"""django_simple_third_party_jwt_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import include
from django.conf import settings

urlpatterns = []

################################################################
# app route
urlpatterns += [
    # 3rd party login
    # here no need to add prefix "api" because it has been set in `settings.py` named JWT_3RD_PREFIX
    path("", include("django_simple_third_party_jwt.urls")),
]
################################################################



# --------------- DEMO DASHBOARD
urlpatterns += [
    # admin
    path("api/__hidden_admin/", admin.site.urls),
    # debug dashboard
    path("api/__hidden_dev_dashboard/", include("dev_dashboard.urls")),
]
# ------------------------------

# --------------- JWT
from rest_framework_simplejwt.views import (
    TokenVerifyView, TokenObtainPairView, TokenRefreshView
)
urlpatterns += [
    path("api/auth/token", TokenObtainPairView.as_view(), name="token_get"),
    path("api/auth/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/verify", TokenVerifyView.as_view(), name="token_verify"),
]
# ---------------------------------



# ----------------------- Swagger for DEMO
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny, IsAdminUser
schema_view = get_schema_view(
    openapi.Info(
        title="DEV DASHBOARD API",
        default_version="v1",
        description="DEV API",
    ),
    public=True,
    permission_classes=(AllowAny,)
    #permission_classes = (IsAdminUser,) # 限制is_staff才可使用
)

urlpatterns += [
    re_path(
        r"^api/__hidden_swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/__hidden_swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^api/__hidden_redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
# --------------------------------------------
