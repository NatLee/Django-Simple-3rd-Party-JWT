# Django Simple 3rd Party JWT

[![Test](https://github.com/NatLee/django-simple-third-party-jwt/actions/workflows/test.yml/badge.svg)](https://github.com/NatLee/django-simple-third-party-jwt/actions/workflows/test.yml)[![Release](https://github.com/NatLee/django-simple-third-party-jwt/actions/workflows/release.yml/badge.svg)](https://github.com/NatLee/django-simple-third-party-jwt/actions/workflows/release.yml)

This is a simple tool for 3rd party login with JWT .

## Installation

```bash
pip install django-simple-third-party-jwt
```

Check it in [Pypi](https://pypi.org/project/django-simple-third-party-jwt/).

## Quick Start

### Back end

1. Add `django_simple_third_party_jwt` to your `INSTALLED_APPS` in `settings.py` like this:

```py
INSTALLED_APPS = [
...
'django_simple_third_party_jwt',
]
```

2. Add APP settings to your `settings.py` like this:

```py

from datetime import timedelta

# -------------- START - CORS Setting --------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "http://*.127.0.0.1",
    "http://localhost",
]
# -------------- END - CORS Setting -----------------

# -------------- Start - SimpleJWT Setting --------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=3600),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}
# -------------- END - SimpleJWT Setting --------------

# -------------- START - Google Auth Setting --------------
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
# SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SOCIAL_GOOGLE_CLIENT_ID = (
    "376808175534-d6mefo6b1kqih3grjjose2euree2g3cs.apps.googleusercontent.com" # Here is test client ID used with `localhost:8000`.
)
LOGIN_REDIRECT_URL = "/"
VALID_REGISTER_DOMAINS = ["gmail.com"]
# --------------- END - Google Auth Setting -----------------
```

3. Include the `django_simple_third_party_jwt` URL settings in your project `urls.py` like this:

```py
from django.conf import settings
from django.urls import include
urlpatterns += [
    # google login
    path("api/auth/google/", include("django_simple_third_party_jwt.urls")),
]
```

You also need to include JWT settings in your `urls.py`.

```py
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
```

4. Migrate and test on your server.

- Migrate

```bash
python manage.py migrate django_simple_third_party_jwt
```

- Test

```bash
python manage.py runserver
```

### Front End

You need to check `{{ social_google_client_id }}` is the same with `Metadata` and your `Html` page.

- Meta

```html
<meta name="google-signin-scope" content="profile email" />
<meta name="google-signin-client_id" content="{{ social_google_client_id }}" />
<script src="https://accounts.google.com/gsi/client" async defer></script>
```

- Html

```html
<li>
    <div id="g_id_onload"
            data-client_id="{{ social_google_client_id }}"
            data-callback="get_jwt_using_google_credential" </div>
    <div class="g_id_signin" data-type="standard" data-size="large" data-theme="outline"
            data-text="sign_in_with" data-shape="rectangular" data-logo_alignment="left">
    </div>
</li>
```

- Javascript

You can try this script to get credential token from Google and verify it with calling our custom 3rd party API.

```html
<script>
  function get_jwt_using_google_credential(data) {
    const credential = data.credential;
    $.ajax({
      method: "POST",
      url: "/api/auth/google/token",
      data: { credential: credential },
    }).done(function (data) {
      const access_token = data.access;
      const refresh_token = data.refresh_token;
      localStorage.setItem("access", access_token);
      localStorage.setItem("refresh", refresh_token);
      console.log("Google Login");
      $.ajax({
        type: "POST",
        url: "/api/auth/token/verify",
        data: { token: access_token },
        headers: {
          Authorization: "Bearer" + " " + access_token,
        },
        success: function (data) {
          var json_string = JSON.stringify(data, null, 2);
          if (json_string) {
            console.log("Token verified successfully!");
          }
        },
        error: function (data) {
          var result = "please login " + data.responseText;
          console.log(result);
        },
      });
    });
  }
</script>
```
