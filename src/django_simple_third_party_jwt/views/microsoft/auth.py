import uuid
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from django_simple_third_party_jwt import settings as jwt_settings
from django_simple_third_party_jwt.models import SocialAccount

from django_simple_third_party_jwt.views.microsoft.msal_helpers import get_sign_in_flow, get_token_from_code, remove_user_and_token
from django_simple_third_party_jwt.views.microsoft.utils import get_user

import logging

logger = logging.getLogger(__name__)

def sign_in(request):
    root_url = request.build_absolute_uri('/')
    flow = get_sign_in_flow(root_url)
    try:
        request.session['auth_flow'] = flow
    except Exception as e:
        print(e)
    return HttpResponseRedirect(flow['auth_uri'])

def sign_out(request):
    remove_user_and_token(request)
    return HttpResponseRedirect(reverse('microsoft-signin'))

def callback(request):
    try:
        result = get_token_from_code(request)
        access_token = result['access_token']
        email = result['id_token_claims']['preferred_username']
    except Exception as e:
        logger.error(f"[AUTH][MICROSOFT] {e}")
        return render_error(request, '')

    user_info = get_user(access_token)
    user_info['email'] = email
    username, domain = email.split('@')

    if domain not in jwt_settings.VALID_REGISTER_DOMAINS:
        logger.warning(f"[AUTH][MICROSOFT] `{email}` attempts to register!!")
        return render_error(request, email)

    user = get_or_create_user(email, username)
    login(request, user)
    refresh = RefreshToken.for_user(user)

    return render(
        request,
        'microsoft/index.html',
        {
            'email': email,
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "description": 'Welcome!',
            "redirect_url": jwt_settings.LOGIN_REDIRECT_URL,
            "access_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY,
            "refresh_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY
        }
    )

def get_or_create_user(email, username):
    try:
        social_account = SocialAccount.objects.get(provider='microsoft', unique_id=email)
        user = social_account.user
        logger.debug(f"[AUTH][MICROSOFT] Existing user logged in: [{user.username}] - [{email}]")
    except SocialAccount.DoesNotExist:
        if User.objects.filter(username=username).exists():
            logger.debug(f"[AUTH][MICROSOFT] Existing username: [{username}]")
            username = str(uuid.uuid4())
            logger.debug(f"[AUTH][MICROSOFT] Creating new username: [{username}]")

        user = User.objects.create_user(username=username, email=email)
        SocialAccount.objects.create(user=user, provider='microsoft', unique_id=email)
        logger.debug(f"[AUTH][MICROSOFT] Created new user: [{username}] - [{email}]")

    return user

def render_error(request, email):
    return render(
        request,
        'microsoft/index.html',
        {
            'email': email,
            "refresh_token": '',
            "access_token": '',
            "description": 'You are not allowed to access this! :(' if email else 'There are something went wrong! :(',
            "redirect_url": jwt_settings.LOGIN_REDIRECT_URL,
            "access_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY,
            "refresh_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY
        }
    )
