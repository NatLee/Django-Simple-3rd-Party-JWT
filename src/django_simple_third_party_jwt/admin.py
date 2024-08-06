from django.contrib import admin
from django_simple_third_party_jwt.models import SocialAccount

@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    """
    SocialAccount 模型的管理UI配置
    """

    # 可搜索的字段
    search_fields = ['user__username', 'user__email', 'provider', 'unique_id']

    # 過濾器
    list_filter = ('provider',)

    # 每頁顯示的條目數
    list_per_page = 25

    # 只讀字段（在編輯頁面中不可修改）
    readonly_fields = ('unique_id',)

    # 在列表頁中可以直接編輯的字段
    list_editable = ('provider',)

    # 自定義顯示方法
    def user_email(self, obj):
        """
        顯示使用者的Email
        """
        return obj.user.email
    user_email.short_description = '使用者Email'

    # 將自定義方法添加到 list_display
    list_display = ("user", "user_email", "provider", "unique_id")
