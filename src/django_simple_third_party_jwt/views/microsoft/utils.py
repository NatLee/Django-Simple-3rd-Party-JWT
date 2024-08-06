import requests
from django_simple_third_party_jwt import settings as jwt_settings

graph_url = 'https://graph.microsoft.com/v1.0'
callback_url = jwt_settings.JWT_3RD_PREFIX + '/auth/microsoft/callback'

def get_user(token):
    user = requests.get(
        '{0}/me'.format(graph_url),
        headers={'Authorization': 'Bearer {0}'.format(token)},
        params={'$select': 'displayName'}
    )
    return user.json()
