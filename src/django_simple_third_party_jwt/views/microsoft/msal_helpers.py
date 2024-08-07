import msal
from django_simple_third_party_jwt import settings as jwt_settings

settings = {
    'app_id': jwt_settings.SOCIAL_MICROSOFT_CLIENT_ID,
    'app_secret': jwt_settings.SOCIAL_MICROSOFT_CLIENT_SECRET,
    'authority': "https://login.microsoftonline.com/common",
    'scopes': ['user.read'],
}

callback_url = jwt_settings.JWT_3RD_PREFIX + '/auth/microsoft/callback'

def load_cache(request):
    cache = msal.SerializableTokenCache()
    if request.session.get('token_cache'):
        cache.deserialize(request.session['token_cache'])
    return cache

def save_cache(request, cache):
    if cache.has_state_changed:
        request.session['token_cache'] = cache.serialize()

def get_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        settings['app_id'],
        authority=settings['authority'],
        client_credential=settings['app_secret'],
        token_cache=cache
    )

def get_sign_in_flow(root_url):
    auth_app = get_msal_app()
    return auth_app.initiate_auth_code_flow(
        settings['scopes'],
        redirect_uri=root_url + callback_url
    )

def get_token_from_code(request):
    cache = load_cache(request)
    auth_app = get_msal_app(cache)
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
            account=accounts[0]
        )
        save_cache(request, cache)
        return result['access_token']

def remove_user_and_token(request):
    if 'token_cache' in request.session:
        del request.session['token_cache']
    if 'user' in request.session:
        del request.session['user']
