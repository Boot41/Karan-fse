from django.contrib import admin
from .models import (
    UserProfile, Portfolio, Investment,
    StockAlert, AIRecommendation, StockData,
    AIAnalysis
)

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'risk_tolerance', 'investment_horizon', 'created_at')
    search_fields = ('user__username',)

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'description')
    search_fields = ('name', 'user__username')

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'symbol', 'shares', 'entry_price', 'entry_date')
    search_fields = ('symbol', 'portfolio__name')
    list_filter = ('entry_date',)

@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'symbol', 'alert_type', 'price_threshold', 'is_active')
    search_fields = ('symbol', 'user__username')
    list_filter = ('alert_type', 'is_active')

@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'symbol', 'confidence_score', 'created_at')
    search_fields = ('symbol', 'user__username')
    list_filter = ('created_at',)

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'current_price', 'daily_high', 'daily_low', 'last_updated')
    search_fields = ('symbol', 'name')
    list_filter = ('last_updated',)

@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'query', 'created_at')
    search_fields = ('query', 'user__username')
    list_filter = ('provider', 'created_at')
