from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Portfolio, Investment, StockData, AIRecommendation

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    risk_tolerance = serializers.IntegerField(required=True)
    investment_goal = serializers.CharField(required=True)
    preferred_investment_duration = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'risk_tolerance', 
                 'investment_goal', 'preferred_investment_duration')

    def create(self, validated_data):
        # Extract UserProfile data
        risk_tolerance = validated_data.pop('risk_tolerance')
        investment_goal = validated_data.pop('investment_goal')
        preferred_investment_duration = validated_data.pop('preferred_investment_duration')

        # Create User instance
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        # Create associated UserProfile
        UserProfile.objects.create(
            user=user,
            risk_tolerance=risk_tolerance,
            investment_goal=investment_goal,
            preferred_investment_duration=preferred_investment_duration
        )

        return user

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('id', 'name', 'description', 'total_value', 'created_at', 'updated_at')
        read_only_fields = ('total_value', 'created_at', 'updated_at')

    def create(self, validated_data):
        # Automatically set the user from the request
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class InvestmentSerializer(serializers.ModelSerializer):
    current_value = serializers.SerializerMethodField()
    profit_loss = serializers.SerializerMethodField()
    
    class Meta:
        model = Investment
        fields = ('id', 'portfolio', 'stock_symbol', 'quantity', 
                 'purchase_price', 'purchase_date', 'current_price',
                 'current_value', 'profit_loss', 'last_updated')
        read_only_fields = ('current_price', 'last_updated')

    def get_current_value(self, obj):
        return obj.quantity * obj.current_price

    def get_profit_loss(self, obj):
        return (obj.current_price - obj.purchase_price) * obj.quantity

class StockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = ('symbol', 'company_name', 'current_price', 'daily_high',
                 'daily_low', 'volume', 'market_cap', 'pe_ratio',
                 'dividend_yield', 'last_updated')

class AIRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRecommendation
        fields = ('id', 'stock_symbol', 'recommendation_type',
                 'confidence_score', 'reasoning', 'created_at',
                 'valid_until')
        read_only_fields = ('created_at', 'valid_until')

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'risk_tolerance', 'investment_goal',
                 'preferred_investment_duration', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
