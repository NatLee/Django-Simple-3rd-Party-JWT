from django.test import TestCase
from mock import Mock, patch

from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from django_simple_third_party_jwt.models import SocialAccount
from django_simple_third_party_jwt.admin import SocialAccountAdmin

from django_simple_third_party_jwt.views.google.token_login import GoogleLogin

class LoginViewTests(TestCase):

    def test_get(self):
        request = Mock()
        request.return_value = {}

        view = GoogleLogin()

        with patch.object(GoogleLogin, 'post') as patched_proxy_method:
            handler = getattr(view, 'post')
            handler(request, credential=123)

        patched_proxy_method.assert_called_once_with(request, credential=123)


class MockRequest:
    pass

class SocialAccountModelTest(TestCase):
    def setUp(self):
        # 創建一個測試　
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # 創建一個　帳號
        self.social_account = SocialAccount.objects.create(
            user=self.user,
            provider='google',
            unique_id='123456789'
        )

    def test_social_account_creation(self):
        """測試第三方帳號的創建"""
        self.assertTrue(isinstance(self.social_account, SocialAccount))
        self.assertEqual(self.social_account.__str__(), f"{self.user.username} - google")

    def test_social_account_fields(self):
        """測試第三方帳號的字段"""
        self.assertEqual(self.social_account.user, self.user)
        self.assertEqual(self.social_account.provider, 'google')
        self.assertEqual(self.social_account.unique_id, '123456789')

class SocialAccountAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = SocialAccountAdmin(SocialAccount, self.site)

        # 創建一個測試使用者
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
        
        # 創建一個第三方帳號
        self.social_account = SocialAccount.objects.create(
            user=self.user,
            provider='google',
            unique_id='123456789'
        )

    def test_list_display(self):
        """測試管理界面的列表顯示"""
        self.assertEqual(list(self.admin.list_display), ["user", "user_email", "provider", "unique_id"])

    def test_search_fields(self):
        """測試管理界面的搜索字段"""
        self.assertEqual(list(self.admin.search_fields), ['user__username', 'user__email', 'provider', 'unique_id'])

    def test_list_filter(self):
        """測試管理界面的過濾器"""
        self.assertEqual(list(self.admin.list_filter), ['provider'])

    def test_readonly_fields(self):
        """測試管理界面的只讀字段"""
        self.assertEqual(list(self.admin.readonly_fields), ['unique_id'])

    def test_user_email_method(self):
        """測試自定義的 user_email 方法"""
        self.assertEqual(self.admin.user_email(self.social_account), 'test@example.com')

class SocialAccountAdminIntegrationTest(TestCase):
    def setUp(self):
        # 建立一個超級使用者
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        self.client.login(username='admin', password='adminpass')

        # 建立一個普通使用者和相關的第三方帳號
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='12345')
        self.social_account = SocialAccount.objects.create(
            user=self.user,
            provider='google',
            unique_id='123456789'
        )

    def test_social_account_list_view(self):
        """測試第三方帳號列表視圖"""
        url = reverse('admin:django_simple_third_party_jwt_socialaccount_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'google')

    def test_social_account_change_view(self):
        """測試第三方帳號修改視圖"""
        url = reverse('admin:django_simple_third_party_jwt_socialaccount_change', args=[self.social_account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'google')
        self.assertContains(response, '123456789')

