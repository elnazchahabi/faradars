from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, LoginHistory, MobileOTP

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_instructor', 'profile_thumbnail', 'is_email_verified', 'is_mobile_verified')
    search_fields = ('username', 'email', 'mobile')
    list_filter = ('is_instructor', 'role', 'is_active', 'is_email_verified', 'is_mobile_verified')

    def profile_thumbnail(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%;" />', obj.profile_image.url
            )
        return "-"
    profile_thumbnail.short_description = 'Profile'

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'ip_address', 'user_agent')
    search_fields = ('user__username', 'ip_address', 'user_agent')
    list_filter = ('login_time',)

@admin.register(MobileOTP)
class MobileOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_used')
    search_fields = ('user__username', 'user__mobile', 'code')
    list_filter = ('created_at', 'is_used')

