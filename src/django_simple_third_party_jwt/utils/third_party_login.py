from django.contrib.auth import login
from rest_framework.response import Response

from django_simple_third_party_jwt.exception import InvalidEmailError
from django_simple_third_party_jwt.utils.get_tokens_for_user import get_tokens_for_user

import logging
logger = logging.getLogger(__name__)

def third_party_login(serializer, request, session=False):
    if serializer.is_valid(raise_exception=True):
        try:
            user = serializer.save()
            if session:
                login(request=request, user=user)
            return Response(get_tokens_for_user(user))
        except InvalidEmailError:
            return Response({
                    "status": "error",
                    "detail": "This email is invalid."
                }, status=401
            )
        except ValueError as exception:
            logger.error(exception)
            return Response({
                    "status": "error",
                    "detail": "Something went wrong :("
                },status=500
            )
    else:
        return Response({
                "status": "error",
                "detail": "Data is not serializable"
            }, status=401
        )




