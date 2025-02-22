from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_active', 'date_joined')
    search_fields = ('email', 'username')
    ordering = ('email',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'risk_tolerance', 'investment_style', 'investment_goal', 'investment_experience')
    search_fields = ('full_name', 'user__email')
    list_filter = ('investment_goal', 'investment_style', 'investment_experience')
