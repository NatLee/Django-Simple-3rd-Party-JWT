from django.urls import path
from dev_dashboard import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register", views.register, name="register"),

    path("login", views.login, name="login"),
    path("logout", views.logout, name="session-logout"),
]
