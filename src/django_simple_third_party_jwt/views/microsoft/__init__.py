import uuid
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken

import msal
import requests

from django_simple_third_party_jwt import settings as jwt_settings
from django_simple_third_party_jwt.models import SocialAccount

import logging

logger = logging.getLogger(__name__)

graph_url = 'https://graph.microsoft.com/v1.0'
callback_url = jwt_settings.JWT_3RD_PREFIX + '/auth/microsoft/callback'

settings = {
    'app_id': jwt_settings.SOCIAL_MICROSOFT_CLIENT_ID,
    'app_secret': jwt_settings.SOCIAL_MICROSOFT_CLIENT_SECRET,
    'authority': "https://login.microsoftonline.com/common",
    'scopes': ['user.read'],
}

def load_cache(request):
  # Check for a token cache in the session
  cache = msal.SerializableTokenCache()
  if request.session.get('token_cache'):
    cache.deserialize(request.session['token_cache'])
  return cache

def save_cache(request, cache):
  # If cache has changed, persist back to session
  if cache.has_state_changed:
    request.session['token_cache'] = cache.serialize()

def get_msal_app(cache=None):
  # Initialize the MSAL confidential client
  auth_app = msal.ConfidentialClientApplication(
    settings['app_id'],
    authority=settings['authority'],
    client_credential=settings['app_secret'],
    token_cache=cache)
  return auth_app

# Method to generate a sign-in flow
def get_sign_in_flow(root_url):
  auth_app = get_msal_app()
  return auth_app.initiate_auth_code_flow(
    settings['scopes'],
    redirect_uri=root_url + callback_url
  )

# Method to exchange auth code for access token
def get_token_from_code(request):
  cache = load_cache(request)
  auth_app = get_msal_app(cache)

  # Get the flow saved in session
  flow = request.session.pop('auth_flow', {})
  result = auth_app.acquire_token_by_auth_code_flow(flow, request.GET)
  save_cache(request, cache)

  return result

def get_token(request):
  cache = load_cache(request)
  auth_app = get_msal_app(cache)

  accounts = auth_app.get_accounts()
  if accounts:
    result = auth_app.acquire_token_silent(
      settings['scopes'],
      account=accounts[0])
    save_cache(request, cache)

    return result['access_token']

def remove_user_and_token(request):
  if 'token_cache' in request.session:
    del request.session['token_cache']

  if 'user' in request.session:
    del request.session['user']

def get_user(token):
    # Send GET to /me
    user = requests.get('{0}/me'.format(graph_url),
    headers={'Authorization': 'Bearer {0}'.format(token)},
    params={'$select':'displayName'})
    return user.json()

def initialize_context(request):
    context = {}
    error = request.session.pop('flash_error', None)
    context['errors'] = []
    if error:
        context['errors'].append(error)
    # Check for user in the session
    context['user'] = request.session.get('user',{'is_authenticated': False})
    return context

def sign_in(request):
    # Get the sign-in flow
    root_url = request.build_absolute_uri('/')
    flow = get_sign_in_flow(root_url)
    # Save the expected flow so we can use it in the callback
    try:
        request.session['auth_flow'] = flow
    except Exception as e:
        print(e)
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(flow['auth_uri'])

def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)
    return HttpResponseRedirect(reverse('microsoft-signin'))

def callback(request):

    try:
        result = get_token_from_code(request)
        access_token = result['access_token']
        email = result['id_token_claims']['preferred_username']

    except Exception as e:
        logger.error(f"[AUTH][MICROSOFT] {e}")
        return render(
            request,
            'microsoft/index.html',
            {
                'email': '',
                "refresh_token": '',
                "access_token": '',
                "description": 'There are something went wrong! :(',
                "redirect_url": jwt_settings.LOGIN_REDIRECT_URL,
                "access_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY,
                "refresh_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY
            }
        )

    # Get the user's profile
    user_info = get_user(access_token)
    user_info['email'] = email
    username, domain = email.split('@')

    if domain not in jwt_settings.VALID_REGISTER_DOMAINS:
        logger.warning(f"[AUTH][MICROSOFT] `{email}` attempts to register!!")
        return render(
            request,
            'microsoft/index.html',
            {
                'email': email,
                "refresh_token": '',
                "access_token": '',
                "description": 'You are not allowed to access this! :(',
                "redirect_url": jwt_settings.LOGIN_REDIRECT_URL,
                "access_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY,
                "refresh_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY
            }
        )

    # 檢查是否存在對應的 Microsoft SocialAccount
    try:
        social_account = SocialAccount.objects.get(provider='microsoft', unique_id=email)
        user = social_account.user
        logger.debug(f"[AUTH][MICROSOFT] Existing user logged in: [{user.username}] - [{email}]")
    except SocialAccount.DoesNotExist:
        # 如果不存在，創建新的 User 和 SocialAccount
        # 如果username已存在，則使用uuid生成一個新的username
        if User.objects.filter(username=username).exists():
          username = str(uuid.uuid4())

        user = User.objects.create_user(
            username=username,
            email=email,
        )
        SocialAccount.objects.create(
            user=user,
            provider='microsoft',
            unique_id=email
        )
        logger.debug(f"[AUTH][MICROSOFT] Created new user: [{username}] - [{email}]")

    # 登入用戶
    login(request, user)

    # 生成 JWT token
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

