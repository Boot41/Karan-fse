from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')
        read_only_fields = ('id',)

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'full_name', 'risk_tolerance',
            'investment_style', 'income_range',
            'investment_goal', 'investment_experience',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
