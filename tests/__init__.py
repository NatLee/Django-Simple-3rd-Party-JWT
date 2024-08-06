# tests/__init__.py

import os
import django
from django.conf import settings

# 設定 DJANGO_SETTINGS_MODULE 環境變量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

# 初始化 Django
django.setup()
