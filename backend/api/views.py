from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from rest_framework.authtoken.models import Token
from .models import UserProfile
from .serializers import UserProfileSerializer, UserRegistrationSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Please provide both email and password'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    # Try to find user by email first
    try:
        user = User.objects.get(email=email)
        username = user.username
    except User.DoesNotExist:
        username = email  # If no user found by email, use email as username
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        })
    else:
        return Response({'error': 'Invalid credentials'}, 
                      status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Create an empty profile for the user
        UserProfile.objects.create(user=user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def market_trends(request):
    # Simulated market data
    trends = [
        {
            'description': 'Tech stocks showing strong momentum',
            'date': '2025-02-23'
        },
        {
            'description': 'Emerging markets present growth opportunities',
            'date': '2025-02-23'
        },
        {
            'description': 'Renewable energy sector gaining traction',
            'date': '2025-02-23'
        }
    ]
    
    recommendations = [
        {
            'title': 'Technology Sector',
            'description': 'Consider increasing exposure to AI and cloud computing companies'
        },
        {
            'title': 'Green Energy',
            'description': 'Solar and wind energy companies show promising growth potential'
        },
        {
            'title': 'Risk Management',
            'description': 'Maintain a diversified portfolio with both growth and value stocks'
        }
    ]
    
    return Response({
        'trends': trends,
        'recommendations': recommendations
    })

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def create(self, request):
        try:
            # Check if profile exists
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile, data=request.data)
        except UserProfile.DoesNotExist:
            # Create new profile
            serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        profile = serializer.save(user=request.user)
        
        return Response(self.get_serializer(profile).data)

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=404)

    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
