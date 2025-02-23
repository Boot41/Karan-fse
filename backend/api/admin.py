from django.contrib import admin
from .models import UserProfile, Portfolio, MarketData

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'risk_tolerance', 'investment_style', 'experience_level', 'investment_horizon']
    list_filter = ['risk_tolerance', 'experience_level']
    search_fields = ['user__email', 'user__username']
    ordering = ('-created_at',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock_symbol', 'purchase_price', 'quantity', 'total_value', 'purchase_date']
    list_filter = ['purchase_date']
    search_fields = ['user__email', 'stock_symbol']

@admin.register(MarketData)
class MarketDataAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'current_price', 'daily_change', 'volume', 'sentiment_score']
    list_filter = ['symbol']
    search_fields = ['symbol']
    ordering = ['-timestamp']
