from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# 登入成功後的重定向 URL
# 如果在 Django 主設置中未定義，則默認為根路徑 "/"
LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL", "/")

# JWT 訪問路徑的前綴
# 通常是 /api
JWT_3RD_PREFIX = getattr(settings, "JWT_3RD_PREFIX", '')

# 允許註冊的電子郵件域名列表
# 這裡設定一些常見的郵件服務提供商作為默認值
VALID_REGISTER_DOMAINS = getattr(
    settings,
    "VALID_REGISTER_DOMAINS",
    [
        'gmail.com',
        'outlook.com',
        'hotmail.com',
        'live.com',
    ]
)

# Google OAuth 2.0 客戶端 ID
# 注意：這是一個測試用的 ID，在生產環境中應該使用自己的使用者端 ID
# https://console.cloud.google.com/apis/credentials
__DEV_GOOGLE_CLIENT_ID = '376808175534-d6mefo6b1kqih3grjjose2euree2g3cs.apps.googleusercontent.com'
SOCIAL_GOOGLE_CLIENT_ID = getattr(
    settings,
    "SOCIAL_GOOGLE_CLIENT_ID",
    __DEV_GOOGLE_CLIENT_ID,
)

if __DEV_GOOGLE_CLIENT_ID == SOCIAL_GOOGLE_CLIENT_ID:
    logger.warning("")
    logger.warning("Using default Google client ID. Please set your own client ID in production.")
    logger.warning("Regist your Google client ID at https://console.cloud.google.com/apis/credentials")
    logger.warning("")

# =====================
# Microsoft OAuth 設置

# Microsoft 應用程序（使用者端）ID
# 注意：這是一個測試用的 ID，在生產環境中應該使用自己的客戶端 ID
# https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps
__DEV_MICROSOFT_CLIENT_ID = '32346173-22bc-43b2-b6ed-f88f6a76e38c'
SOCIAL_MICROSOFT_CLIENT_ID = getattr(
    settings,
    "SOCIAL_MICROSOFT_CLIENT_ID",
    __DEV_MICROSOFT_CLIENT_ID,
)

if __DEV_MICROSOFT_CLIENT_ID == SOCIAL_MICROSOFT_CLIENT_ID:
    logger.warning("")
    logger.warning("Using default Microsoft client ID. Please set your own client ID in production.")
    logger.warning("Regist your Microsoft client ID at https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps")
    logger.warning("")


# Microsoft 客戶端密鑰
# 注意：這是一個測試用的密鑰，在生產環境中應該使用自己的使用者端密鑰
# 警告：使用者端密鑰應該保密，不應該在版本控制中公開
__DEV_MICROSOFT_CLIENT_SECRET = 'K5z8Q~dIXDiFN5qjMjRjIx34cZOJ3Glkrg.dxcG9'
SOCIAL_MICROSOFT_CLIENT_SECRET = getattr(
    settings,
    "SOCIAL_MICROSOFT_CLIENT_SECRET",
    __DEV_MICROSOFT_CLIENT_SECRET,
)

if __DEV_MICROSOFT_CLIENT_SECRET == SOCIAL_MICROSOFT_CLIENT_SECRET:
    logger.warning("")
    logger.warning("Using default Microsoft client secret. Please set your own client secret in production.")
    logger.warning("Regist your Microsoft client secret at https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps")
    logger.warning("")


# 用於在本地儲存中保存 Microsoft access token 的鍵名
MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY = getattr(
    settings,
    "MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY",
    'access_token'
)

# 用於在本地儲存中保存 Microsoft refresh token 的鍵名
MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY = getattr(
    settings,
    "MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY",
    'refresh_token'
)

# =====================

# 使用示例：

# 1. 檢查使用者的電子郵件域名是否允許註冊
# def is_valid_email_domain(email):
#     _, domain = email.split('@')
#     return domain in VALID_REGISTER_DOMAINS

# 2. 在視圖中使用 LOGIN_REDIRECT_URL
# from django.shortcuts import redirect
# def login_view(request):
#     # 登入邏輯...
#     return redirect(LOGIN_REDIRECT_URL)

# 3. 使用 Google 客戶端 ID 進行 OAuth 認證
# from google.oauth2 import id_token
# from google.auth.transport import requests
# def verify_google_token(token):
#     try:
#         idinfo = id_token.verify_oauth2_token(token, requests.Request(), SOCIAL_GOOGLE_CLIENT_ID)
#         return idinfo
#     except ValueError:
#         return None

# 4. 使用 Microsoft 客戶端 ID 和密鑰進行 OAuth 認證
# import requests
# def get_microsoft_token(code):
#     token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
#     data = {
#         "client_id": SOCIAL_MICROSOFT_CLIENT_ID,
#         "client_secret": SOCIAL_MICROSOFT_CLIENT_SECRET,
#         "code": code,
#         "grant_type": "authorization_code",
#         "redirect_uri": "your_redirect_uri"
#     }
#     response = requests.post(token_url, data=data)
#     return response.json()

# 5. 在前端儲存 Microsoft tokens
# // JavaScript 代碼
# localStorage.setItem(MICROSOFT_JWT_REDIRECT_ACCESS_TOKEN_KEY, access_token);
# localStorage.setItem(MICROSOFT_JWT_REDIRECT_REFRESH_TOKEN_KEY, refresh_token);


