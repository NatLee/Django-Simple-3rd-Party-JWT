import django
from django.conf import settings
from django.urls import path

settings.configure(
    SECRET_KEY='test',
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:"
        }
    },
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.sites",
        "rest_framework",
        "django_simple_third_party_jwt",
    ],
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    ROOT_URLCONF='tests.urls',
    SITE_ID=1,
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
    },

    # -------------- START - Google Auth Setting --------------
    SECURE_REFERRER_POLICY = "no-referrer-when-downgrade",
    SECURE_CROSS_ORIGIN_OPENER_POLICY = None,
    SOCIAL_GOOGLE_CLIENT_ID = (
        "376808175534-d6mefo6b1kqih3grjjose2euree2g3cs.apps.googleusercontent.com"
    ),
    LOGIN_REDIRECT_URL = "/",
    VALID_REGISTER_DOMAINS = ["gmail.com"],
    # --------------- END - Google Auth Setting -----------------
)

# 創建一個簡單的 URL 配置
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
]

django.setup()
