
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status, viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .models import UserProfile, Portfolio, MarketData
from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    ForgotPasswordSerializer, 
    UserProfileSerializer, 
    PortfolioSerializer, 
    MarketDataSerializer,
    LogoutSerializer
)

# ✅ User Registration API
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ User Login API (JWT Token Generation)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Authenticate user and return JWT token"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

# ✅ User Logout API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logout user by blacklisting refresh token."""
    try:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ✅ Forgot Password API
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """Send password reset instructions"""
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        return Response({'message': 'Password reset instructions sent'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ User Profile ViewSet
class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user profiles.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

# ✅ Portfolio ViewSet
class PortfolioViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user portfolios.
    """
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

# ✅ Market Data ViewSet
class MarketDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fetching and managing market data.
    """
    queryset = MarketData.objects.all()
    serializer_class = MarketDataSerializer
    permission_classes = [IsAuthenticated]

# ✅ Logout View
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data["refresh"]
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
                return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ User Profile View
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)