from django.urls import path

from django.conf import settings

from django_simple_third_party_jwt.views.google.token_login import GoogleLogin
from django_simple_third_party_jwt.views.google.session_login import GoogleLoginSession

from django_simple_third_party_jwt.views import microsoft


urlpatterns = [
    path(f"{settings.JWT_3RD_PREFIX}/auth/google/token", GoogleLogin.as_view(), name='google-token'),
    path(f"{settings.JWT_3RD_PREFIX}/auth/google/token/session", GoogleLoginSession.as_view(), name='google-token-session'),
]

urlpatterns += [
    path(f"{settings.JWT_3RD_PREFIX}/auth/microsoft/signin", microsoft.sign_in, name='microsoft-signin'),
    path(f"{settings.JWT_3RD_PREFIX}/auth/microsoft/signout", microsoft.sign_out, name='microsoft-signout'),
    path(f"{settings.JWT_3RD_PREFIX}/auth/microsoft/callback", microsoft.callback, name='microsoft-callback'),
]
