from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import UserProfile, Portfolio, MarketData
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

# 🎯 User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    INVESTMENT_TYPE_CHOICES = [
        ('short-term', 'Short-term'),
        ('mid-term', 'Mid-term'),
        ('long-term', 'Long-term'),
    ]

    INVESTMENT_REASON_CHOICES = [
        ('wealth growth', 'Wealth Growth'),
        ('education', 'Education'),
        ('retirement', 'Retirement'),
        ('estate', 'Estate'),
    ]

    INCOME_RANGE_CHOICES = [
        ('under 2 LPA', 'Under 2 LPA'),
        ('2 LPA - 5 LPA', '2 LPA - 5 LPA'),
        ('5 LPA - 10 LPA', '5 LPA - 10 LPA'),
        ('10 LPA - 15 LPA', '10 LPA - 15 LPA'),
        ('15 LPA - 20 LPA', '15 LPA - 20 LPA'),
        ('20 LPA+', '20 LPA+'),
    ]

    INVESTMENT_EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    class Meta:
        model = UserProfile
        fields = (
            'id',
            'email',
            'name',
            'risk_tolerance',
            'investment_type',
            'investment_reason',
            'income_range',
            'investment_experience',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'email', 'created_at', 'updated_at')

    investment_type = serializers.ChoiceField(choices=INVESTMENT_TYPE_CHOICES)
    investment_reason = serializers.ChoiceField(choices=INVESTMENT_REASON_CHOICES)
    income_range = serializers.ChoiceField(choices=INCOME_RANGE_CHOICES)
    investment_experience = serializers.ChoiceField(choices=INVESTMENT_EXPERIENCE_CHOICES)

# 🎯 Logout Serializer
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        """Ensure refresh token is provided"""
        if "refresh" not in data:
            raise serializers.ValidationError("Refresh token is required.")
        return data

# 🎯 Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'password']  # Only email and password fields are required

    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def create(self, validated_data):
        """Create a new user"""
        # Generate a username from the email or use a default one
        username = validated_data['email'].split('@')[0]  # Use part before '@' as username

        user = User.objects.create_user(
            username=username,  # Automatically set username from email
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

# 🎯 Login Serializer (Email & Password)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid email"})

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError({"error": "Invalid credentials"})

        # Check if the user has a profile
        profile, created = UserProfile.objects.get_or_create(user=user)

        # If the profile was just created (new user), it might be incomplete
        if created:
            raise serializers.ValidationError({"error": "Profile is incomplete. Please complete your profile."})

        # Create JWT tokens for the user
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }

# 🎯 Forgot Password Serializer
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

# 🎯 Reset Password Serializer
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=6, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

# 🎯 User Serializer (For Returning User Details)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')

# 🎯 Portfolio Serializer
class PortfolioSerializer(serializers.ModelSerializer):
    total_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    profit_loss = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Portfolio
        fields = (
            'id',
            'stock_symbol',
            'purchase_price',
            'quantity',
            'total_value',
            'current_price',
            'profit_loss',
            'purchase_date',
            'last_updated',
            'notes'
        )
        read_only_fields = ('id', 'purchase_date', 'last_updated')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            market_data = MarketData.objects.filter(
                stock_symbol=instance.stock_symbol
            ).latest('timestamp')
            data['current_price'] = str(market_data.current_price)
            current_value = instance.quantity * market_data.current_price
            purchase_value = instance.quantity * instance.purchase_price
            data['profit_loss'] = str(current_value - purchase_value)
        except MarketData.DoesNotExist:
            data['current_price'] = str(instance.purchase_price)
            data['profit_loss'] = '0.00'
        return data

# 🎯 Market Data Serializer
class MarketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketData
        fields = (
            'id',
            'stock_symbol',
            'timestamp',
            'current_price',
            'daily_change',
            'volume',
            'high_52_week',
            'low_52_week',
            'sentiment_score'
        )
        read_only_fields = ('id', 'timestamp')