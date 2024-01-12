
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken

from loguru import logger

import msal
import requests

from django_simple_third_party_jwt import settings as jwt_settings
from django_simple_third_party_jwt.models import SocialAccount

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
    # Make the token request
    try:
        result = get_token_from_code(request)
    except ValueError:
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

    access_token = result['access_token']
    email = result['id_token_claims']['preferred_username']

    # Get the user's profile
    user = get_user(access_token)
    user['email'] = email
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

    # 判斷是否有同樣的使用者名稱
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 如果沒有，則建立一個新的使用者
        user = User.objects.create_user(
            username=username,
            email=email,
        )
        # 建立 SocialAccount
        SocialAccount(
          user=user,
          provider='microsoft', # 使用 Microsoft 登入
          unique_id=email
        ).save()
        logger.debug(f"[AUTH][MICROSOFT] Created user [{username}] - [{email}]")

    # 判斷是否有使用 Microsoft 註冊過的 SocialAccount
    # 因為可能是用其他方式註冊的，所以要檢查
    try:
        SocialAccount.objects.get(user=user, provider="microsoft")
    except SocialAccount.DoesNotExist:
        logger.error(f"[AUTH][MICROSOFT] SocialAccount does not exist")
        return render(
            request,
            'microsoft/index.html',
            {
                'email': email,
                "refresh_token": '',
                "access_token": '',
                "description": 'There is no account associated with this email! :(',
                "redirect_url": jwt_settings.LOGIN_REDIRECT_URL,
                "access_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY,
                "refresh_token_key": jwt_settings.MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY
            }
        )


    refresh = RefreshToken.for_user(user)
    login(request, user)

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
