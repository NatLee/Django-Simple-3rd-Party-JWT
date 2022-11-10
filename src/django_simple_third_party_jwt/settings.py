
from django.conf import settings

# my test client id
SOCIAL_GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_GOOGLE_CLIENT_ID", '376808175534-d6mefo6b1kqih3grjjose2euree2g3cs.apps.googleusercontent.com')

VALID_REGISTER_DOMAINS = getattr(settings, "VALID_REGISTER_DOMAINS", ['gmail.com'])

