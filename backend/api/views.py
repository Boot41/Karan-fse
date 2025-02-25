import requests
import logging
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, Portfolio, MarketData
from .serializers import (
    RegisterSerializer, LoginSerializer, ForgotPasswordSerializer,
    UserProfileSerializer, PortfolioSerializer, MarketDataSerializer
)

# API Keys (Move to environment variables in production)
ALPHA_VANTAGE_API_KEY = "ZRLEESP54OHIGBYP"
FINNHUB_API_KEY = "cutneu1r01qv6ijjalo0cutneu1r01qv6ijjalog"
GEMINI_API_KEY = "AizaSyAQpgRt9PyL3mNlh-ZuNxG2rwykw6UtpAQ"

# Extra words to clean user query
EXTRA_WORDS = ["stock", "share", "price", "value", "company", "market", "buy", "sell", "should", "today", "best", "which", "one", "I"]

def clean_query(query):
    """Removes extra words from user input."""
    words = query.lower().split()
    cleaned = " ".join([word for word in words if word not in EXTRA_WORDS]).strip()
    return cleaned if cleaned else query

def extract_stock_query(user_input):
    """Extracts stock-related keywords from a natural language query."""
    keywords = ["buy", "sell", "invest", "currently", "what is", "can I"]
    words = user_input.lower().split()

    action = next((word for word in words if word in keywords), None)
    stock_name = " ".join(word for word in words if word not in keywords and word.isalpha())

    return action, stock_name.strip()

def search_stock_symbol(query):
    """Finds stock symbol using Finnhub and Alpha Vantage."""
    cleaned_query = clean_query(query)

    # Finnhub API search
    url = f"https://finnhub.io/api/v1/search?q={cleaned_query}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    results = response.get("result", [])

    if results:
        return results[0]["symbol"], results[0]["description"]

    # Alpha Vantage search
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={cleaned_query}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url).json()
    results = response.get("bestMatches", [])

    if results:
        return results[0]["1. symbol"], results[0]["2. name"]

    return None, None

def get_stock_price(symbol):
    """Fetches real-time stock price from Finnhub (fallback to Alpha Vantage)."""
    # Try Finnhub first
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url).json()
    price = response.get("c")

    if price:
        return price, "Finnhub"

    # Fallback to Alpha Vantage
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url).json()
    price = response.get("Global Quote", {}).get("05. price")

    return float(price) if price else None, "Alpha Vantage"

def get_user_profile(user):
    """Fetches user profile details for personalized recommendations."""
    try:
        profile = UserProfile.objects.get(user=user)
        return {
            "risk_tolerance": profile.risk_tolerance,
            "investment_type": profile.investment_type,
            "investment_reason": profile.investment_reason,
            "income_range": profile.income_range,
            "investment_experience": profile.investment_experience
        }
    except UserProfile.DoesNotExist:
        return None

def send_to_gemini(user_data):
    """Sends stock data + user profile to Gemini API for AI-generated recommendations."""
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1:generateText"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": f"""Analyze the following stock data and provide a personalized investment recommendation based on the user's profile:
        
        **User Profile:**
        Risk Tolerance: {user_data["risk_tolerance"]}
        Investment Type: {user_data["investment_type"]}
        Investment Reason: {user_data["investment_reason"]}
        Income Range: {user_data["income_range"]}
        Investment Experience: {user_data["investment_experience"]}

        **Stock Data:**
        Company: {user_data["company"]}
        Stock Symbol: {user_data["symbol"]}
        Current Price: {user_data["price"]} USD
        Data Source: {user_data["source"]}

        Provide a clear and concise recommendation (e.g., Buy, Hold, or Sell) and a short reasoning.""",
        "max_tokens": 150
    }

    response = requests.post(f"{url}?key={GEMINI_API_KEY}", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["candidates"][0]["output"]
    return "Could not generate an AI-based recommendation at the moment."

@api_view(['GET'])
@permission_classes([AllowAny])
def stock_advisory_view(request):
    """Provides stock advisory information based on user input."""
    user_input = request.GET.get("query")
    if not user_input:
        return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)

    action, stock_name = extract_stock_query(user_input)
    if not stock_name:
        return Response({"error": "No stock name found in the query."}, status=status.HTTP_400_BAD_REQUEST)

    # Fetch stock symbol and price using the stock_name
    symbol, company = search_stock_symbol(stock_name)
    if not symbol:
        return Response({"error": f"Could not find relevant stock for '{stock_name}'."}, status=status.HTTP_404_NOT_FOUND)

    price, source = get_stock_price(symbol)
    if price is None:
        return Response({"error": f"Failed to fetch stock price for '{symbol}'."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Construct the response
    advisory_data = {
        "query": user_input,
        "symbol": symbol,
        "company": company,
        "price": price,
        "source": source,
        "advice": f"Consider {action}ing {company} stock." if action else "Here's the information you requested."
    }

    return Response(advisory_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Registers a new user."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Logs in an existing user."""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logs out a user."""
    try:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        RefreshToken(refresh_token).blacklist()
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """Handles password reset requests."""
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        return Response({'message': 'Password reset instructions sent'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Profile API
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def get_profile(self, request):
        """Get profile data on login"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])  # Added POST to create a new profile
    def create_profile(self, request):
        """Create a new user profile"""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 201 for created
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])  # Keep PUT to update an existing profile
    def save_profile(self, request):
        """Save user info from UserInfo.jsx after login"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  # 200 for successful update
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Portfolio API
class PortfolioViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

class MarketDataViewSet(viewsets.ModelViewSet):
    """Handles stock market data."""
    queryset = MarketData.objects.all()
    serializer_class = MarketDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MarketData.objects.all()

@api_view(['PUT'])  # Changed to PUT to match your request
@permission_classes([IsAuthenticated])  # Ensure that only authenticated users can save their profile
def save_profile_view(request):
    """Save user profile data."""
    logger = logging.getLogger(__name__)
    logger.info("Save profile view called")
    user = request.user
    data = request.data  # Profile data from the request

    # Check if the user already has a profile
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Serialize the data and update the profile
    serializer = UserProfileSerializer(profile, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Profile saved successfully."}, status=status.HTTP_200_OK)
    
    logger.error("Profile save failed: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)