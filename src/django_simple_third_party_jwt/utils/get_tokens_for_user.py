
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token),
        # compatibility with official Simple JWT
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
