from django.contrib import admin

# Register your models here.
from django_simple_third_party_jwt.models import SocialAccount


@admin.register(SocialAccount)
class SocialAccount_(admin.ModelAdmin):

    list_display = ("user", "provider", "unique_id")
