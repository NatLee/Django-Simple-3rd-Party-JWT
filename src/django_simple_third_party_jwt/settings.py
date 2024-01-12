
from django.conf import settings

LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL", "/")

JWT_3RD_PREFIX = getattr(settings, "JWT_3RD_PREFIX", '')

VALID_REGISTER_DOMAINS = getattr(settings, "VALID_REGISTER_DOMAINS", ['gmail.com', 'outlook.com', 'hotmail.com', 'live.com'])

# My test Google Client ID
SOCIAL_GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_GOOGLE_CLIENT_ID", '376808175534-d6mefo6b1kqih3grjjose2euree2g3cs.apps.googleusercontent.com')

# =====================
# My test Microsoft Client ID & Secret

# ID
SOCIAL_MICROSOFT_CLIENT_ID = getattr(settings, "SOCIAL_MICROSOFT_CLIENT_ID", '32346173-22bc-43b2-b6ed-f88f6a76e38c')
# Secret
SOCIAL_MICROSOFT_CLIENT_SECRET = getattr(settings, "SOCIAL_MICROSOFT_CLIENT_SECRET", 'K5z8Q~dIXDiFN5qjMjRjIx34cZOJ3Glkrg.dxcG9')

# Key to store the access token in the local storage
MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY = getattr(settings, "MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY", 'access_token')
MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY = getattr(settings, "MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY", 'refresh_token')

# =====================

