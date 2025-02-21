from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, Portfolio, Investment,
    StockAlert, AIRecommendation, StockData, AIAnalysis
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')
        read_only_fields = ('id',)

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'risk_tolerance', 'investment_horizon', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class PortfolioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class InvestmentSerializer(serializers.ModelSerializer):
    portfolio = PortfolioSerializer(read_only=True)
    portfolio_id = serializers.PrimaryKeyRelatedField(
        queryset=Portfolio.objects.all(),
        write_only=True,
        source='portfolio'
    )
    
    class Meta:
        model = Investment
        fields = [
            'id', 'portfolio', 'portfolio_id', 'symbol',
            'shares', 'entry_price', 'entry_date',
            'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class StockAlertSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StockAlert
        fields = [
            'id', 'user', 'symbol', 'alert_type',
            'price_threshold', 'is_active', 'triggered_at',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'triggered_at', 'created_at']

class AIRecommendationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = AIRecommendation
        fields = [
            'id', 'user', 'symbol', 'recommendation',
            'confidence_score', 'analysis_data', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = [
            'id', 'symbol', 'name', 'current_price',
            'daily_high', 'daily_low', 'volume',
            'market_cap', 'pe_ratio', 'dividend_yield',
            'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']

class AIAnalysisSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    provider = serializers.CharField(required=False)  # Make provider optional
    
    class Meta:
        model = AIAnalysis
        fields = ['id', 'user', 'query', 'provider', 'response', 'summary', 'created_at']
        read_only_fields = ['id', 'user', 'response', 'summary', 'created_at']
