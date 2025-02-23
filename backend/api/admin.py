from django.contrib import admin
from .models import UserProfile, Portfolio, MarketData

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'risk_tolerance', 'income_range', 'investment_experience']  # Removed invalid fields
    list_filter = ['risk_tolerance', 'investment_experience']  # Fixed field name
    search_fields = ['user__email', 'user__username']
    ordering = ('-id',)  # Changed 'created_at' to 'id' since 'created_at' doesn't exist

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
