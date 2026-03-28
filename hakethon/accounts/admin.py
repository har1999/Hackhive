from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTP

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['phone', 'name', 'role', 'is_verified', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_active']
    search_fields = ['phone', 'name']
    ordering = ['-date_joined']
    fieldsets = (
        (None, {'fields': ('phone', 'name', 'role', 'password')}),
        ('Status', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'name', 'role', 'password1', 'password2')}),
    )

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['phone', 'code', 'is_used', 'attempts', 'created_at']
    list_filter = ['is_used']
    search_fields = ['phone']
    readonly_fields = ['created_at']
