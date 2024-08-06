from django.db import models
from django.contrib.auth.models import User


class SocialAccount(models.Model):
    """
    第三方帳號模型
    用於儲存使用者的第三方登入訊息
    """

    # provider 字段用於標示第三方登入的提供者
    # 可以擴展以支持其他提供者
    provider = models.CharField(
        max_length=200,
        default="", # 預設值為空字串
        verbose_name="提供者",
        blank=True
    )
    # 註解：provider 的可能值示例：
    # - "google"
    # - "facebook"
    # - "twitter"
    # - "github"

    # unique_id 存儲第三方平台提供的唯一ID
    # 對於 Google，這通常是 sub 字段的值
    unique_id = models.CharField(
        verbose_name="唯一ID",
        max_length=200
    )
    # 註解：unique_id 的示例值：
    # - Google: "123456789012345678901"
    # - Facebook: "1234567890"
    # - Twitter: "12345678"

    # 關聯到 Django 內建的 User 模型
    # 使用 ForeignKey 建立一對多關係：一個 User 可以有多個 SocialAccount
    user = models.ForeignKey(
        User,
        verbose_name="使用者",
        related_name="social",
        on_delete=models.CASCADE
    )
    # 註解：通過 related_name="social"，可以從 User 模型反向查詢：
    # user.social.all() 會返回該用戶的所有 SocialAccount 實例

    class Meta:
        # 指定資料庫表名
        db_table = "social_account"
        # 設定模型在管理界面中的顯示名稱（複數形式）
        verbose_name_plural = "第三方登入（3rd party login）"
        # 設定模型在管理界面中的顯示名稱（單數形式）
        verbose_name = "第三方登入（3rd party login）"

    def __str__(self):
        """
        定義模型的字串表示
        """
        return f"{self.user.username} - {self.provider}"

# 使用範例：

# 1. 建立一個新的 SocialAccount 實例
# user = User.objects.get(username="john_doe")
# social_account = SocialAccount.objects.create(
#     provider="google",
#     unique_id="123456789012345678901",
#     user=user
# )

# 2. 查詢特定使用者的所有第三方帳號
# user_social_accounts = user.social.all()

# 3. 查詢使用特定提供者的所有第三方帳號
# google_accounts = SocialAccount.objects.filter(provider="google")

# 4. 根據 unique_id 查找特定的第三方帳號
# specific_account = SocialAccount.objects.get(unique_id="123456789012345678901")

# 5. 刪除一個第三方帳號（會觸發級聯刪除，但不會刪除關聯的 User）
# social_account.delete()
