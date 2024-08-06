import uuid
from django.contrib.auth.models import User
from rest_framework import serializers
from google.oauth2 import id_token
from google.auth.transport import requests

from django_simple_third_party_jwt import settings
from django_simple_third_party_jwt.models import SocialAccount

from django_simple_third_party_jwt.exception import InvalidEmailError

import logging

logger = logging.getLogger(__name__)

class GoogleLoginSerializer(serializers.Serializer):
    # Google login
    # 用於接收Google返回的憑證
    credential = serializers.CharField(required=True)

    def verify_token(self, credential):
        """
        驗證Google返回的id_token
        credential: JWT格式的字符串
        """
        logger.debug(f"Verify {credential[:50]}...")
        # 使用Google提供的方法驗證token
        idinfo = id_token.verify_oauth2_token(
            credential, requests.Request(), settings.SOCIAL_GOOGLE_CLIENT_ID
        )
        # 驗證token的發行者
        if idinfo["iss"] not in [
            "accounts.google.com",
            "https://accounts.google.com",
        ]:
            logger.error("Wrong issuer")
            raise ValueError("Wrong issuer.")
        # 驗證token的受眾
        if idinfo["aud"] not in [settings.SOCIAL_GOOGLE_CLIENT_ID]:
            logger.error("Could not verify audience")
            raise ValueError("Could not verify audience.")
        # 驗證成功
        logger.info("successfully verified")
        return idinfo

    def create(self, validated_data):
        idinfo = self.verify_token(validated_data.get("credential"))
        if not idinfo:
            raise ValueError("Incorrect Credentials")

        # 從idinfo中提取email
        email = idinfo["email"]
        _, domain = email.split("@")

        # 檢查email域名是否在允許的列表中
        if domain not in settings.VALID_REGISTER_DOMAINS:
            logger.warning(f"[AUTH][GOOGLE] `{email}` attempts to register!!")
            raise InvalidEmailError

        # 首先檢查是否存在對應的 Google SocialAccount
        try:
            social_account = SocialAccount.objects.get(provider='google', unique_id=idinfo["sub"])
            user = social_account.user
            logger.debug(f"[AUTH][GOOGLE] Existing user logged in: [{user.username}] - [{email}]")
        except SocialAccount.DoesNotExist:
            # 如果不存在，創建新的 User 和 SocialAccount
            username = str(uuid.uuid4())
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=idinfo.get("given_name", ""),
                last_name=idinfo.get("family_name", ""),
            )
            SocialAccount.objects.create(
                user=user,
                provider='google',
                unique_id=idinfo["sub"]
            )
            logger.debug(f"[AUTH][GOOGLE] Created new user: [{username}] - [{email}]")

        return user


class UserSerializer(serializers.ModelSerializer):
    """
    用於序列化和反序列化User模型的數據
    """
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


# 註解：以下是一些可能的範例數據

# Google返回的id_token示例（JWT格式）：
# credential = "eyABC.ABC.signature"

# 解碼後的idinfo示例：
# idinfo = {
#     "iss": "https://accounts.google.com",
#     "azp": "123456789-abcdefghijklmnopqrstuvwxyz012345.apps.googleusercontent.com",
#     "aud": "123456789-abcdefghijklmnopqrstuvwxyz012345.apps.googleusercontent.com",
#     "sub": "123456789012345678901",
#     "email": "john.doe@example.com",
#     "email_verified": True,
#     "name": "John Doe",
#     "given_name": "John",
#     "family_name": "Doe",
#     "locale": "en",
#     "iat": 1623123456,
#     "exp": 1623127056
# }

# 建立的User實例示例：
# user = User(
#     username="john.doe",
#     first_name="John",
#     last_name="Doe",
#     email="john.doe@example.com"
# )

# 建立的SocialAccount實例示例：
# social_account = SocialAccount(
#     user=user,
#     provider="google",
#     unique_id="123456789012345678901"
# )
