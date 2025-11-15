from django.contrib import admin
from .models import UserTwoFactorAuth

@admin.register(UserTwoFactorAuth)
class UserTwoFactorAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_enabled', 'created_at', 'updated_at')
    list_filter = ('is_enabled', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'secret_key')
