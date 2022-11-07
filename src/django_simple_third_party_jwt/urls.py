from django.contrib.auth import views as auth_views
from django.urls import path

from django_simple_third_party_jwt import views

urlpatterns = [
    path("token", views.GoogleLogin.as_view(), name='google_token'),
]
