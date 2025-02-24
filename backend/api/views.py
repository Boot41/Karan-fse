from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status, viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
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
#api imports
import requests
from django.http import JsonResponse


def get_stock_price_alpha_vantage(symbol):
    api_key = 'ZRLEESP54OHIGBYP'  # Your Alpha Vantage API key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}'
    
    try:
        # Send the request to the Alpha Vantage API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Parse the JSON response
        data = response.json()

        # Check if the response contains valid data
        if 'Time Series (5min)' in data:
            # Get the latest available time from the time series data
            latest_time = list(data['Time Series (5min)'].keys())[0]
            # Extract the latest stock price (closing price)
            latest_price = data['Time Series (5min)'][latest_time]['4. close']
            return latest_price
        else:
            # If the expected data is not in the response, return None or an error message
            return "Error: Stock data not found."

    except requests.exceptions.RequestException as e:
        # If the request fails (e.g., connection error), print the error
        return f"Request failed: {e}"


def stock_price_view(request, symbol):
    price = get_stock_price_alpha_vantage(symbol)
    return JsonResponse({'symbol': symbol, 'price': price})



def get_stock_price_finhub(symbol):
    api_key = 'cutneu1r01qv6ijjalo0cutneu1r01qv6ijjalog'  # Your Finhub API key
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}'
    
    try:
        # Send the request to the Finhub API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Parse the JSON response
        data = response.json()

        # Extract the current stock price
        if 'c' in data:
            return data['c']  # 'c' is the current price
        else:
            return "Error: Stock data not found."

    except requests.exceptions.RequestException as e:
        # If the request fails (e.g., connection error), print the error
        return f"Request failed: {e}"

def stock_price_finhub_view(request, symbol):
    price = get_stock_price_finhub(symbol)
    return JsonResponse({'symbol': symbol, 'price': price})




# List of known stock symbols (add more as needed)
known_symbols = ['AAPL', 'TSLA', 'GOOG', 'AMZN', 'MSFT', 'FB']


# Helper function to extract stock symbol from the query
def extract_stock_symbol(query):
    query = query.upper()
    for symbol in known_symbols:
        if symbol in query:
            return symbol
    return None

# Function to fetch real-time stock data from Alpha Vantage API
def get_stock_price_alpha_vantage(symbol):
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'  # Replace with your Alpha Vantage API key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    try:
        latest_time = list(data['Time Series (5min)'].keys())[0]
        return data['Time Series (5min)'][latest_time]['4. close']
    except KeyError:
        return None

# Function to fetch real-time stock data from Finnhub API
def get_stock_price_finnhub(symbol):
    api_key = 'YOUR_FINNHUB_API_KEY'  # Replace with your Finnhub API key
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}'
    response = requests.get(url)
    data = response.json()

    try:
        return data['c']  # 'c' stands for current price
    except KeyError:
        return None

# API endpoint to handle the query and fetch stock data
@api_view(['GET'])
def live_stock_data(request, query):
    """
    This view will handle the query and extract the stock symbol,
    then call external APIs to fetch real-time stock data.
    """
    # Step 1: Extract stock symbol from the query
    symbol = extract_stock_symbol(query)

    if not symbol:
        return Response({
            'error': 'Could not extract a stock symbol from your query.'
        }, status=400)

    # Step 2: Fetch stock prices (Alpha Vantage and Finnhub)
    price_alpha_vantage = get_stock_price_alpha_vantage(symbol)
    price_finnhub = get_stock_price_finnhub(symbol)

    if price_alpha_vantage and price_finnhub:
        combined_price = {
            'symbol': symbol,
            'price_alpha_vantage': price_alpha_vantage,
            'price_finnhub': price_finnhub,
            'query': query
        }
        return Response(combined_price)
    else:
        return Response({
            'error': f'Unable to fetch data for {symbol} from both sources.'
        }, status=400)

# Use this API endpoint to fetch stock data with query like "Should I buy Tesla stock?"
@api_view(['GET'])
def get_stock_data_for_query(request, query):
    """
    Endpoint to get combined stock data from multiple APIs (Alpha Vantage and Finnhub).
    """
    # Fetch live stock data from the stock data API
    stock_data = live_stock_data(request, query)

    if stock_data.status_code != 200:
        return stock_data  # Return error if fetching data fails
    
    # Prepare JSON data to be sent to Gemini for summarization
    data_for_gemini = {
        'user_profile': {
            'risk_tolerance': request.user.profile.risk_tolerance,
            'investment_style': request.user.profile.investment_style,
            'income_range': request.user.profile.income_range,
            'investment_reason': request.user.profile.investment_reason
        },
        'stock_data': stock_data.data
    }

    # Send data to Gemini API for summarization (Example URL, modify accordingly)
    gemini_api_url = 'https://api.gemini.com/your-endpoint'
    gemini_api_key = 'YOUR_GEMINI_API_KEY'  # Replace with your Gemini API key
    headers = {'Authorization': f'Bearer {gemini_api_key}'}

    response = requests.post(gemini_api_url, json=data_for_gemini, headers=headers)

    if response.status_code == 200:
        return Response(response.json())  # Return summarized response from Gemini
    else:
        return Response({
            'error': 'Failed to communicate with Gemini API.'
        }, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Summarize portfolio details"""
        portfolio = self.get_queryset()
        total_value = sum(item.value for item in portfolio)  # Example calculation
        return Response({'total_value': total_value})

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

# ✅ User Profile View (Updated for JWT Authentication)
class UserProfileView(generics.RetrieveAPIView):
    """
    Retrieve user profile of the authenticated user.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Ensure user profile exists or create one for the authenticated user
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Serialize the user profile and return the response
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)

# ✅ Update Profile API (PUT profile)
class UserProfileUpdateView(generics.UpdateAPIView):
    """
    Update user profile of the authenticated user.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get the user's profile
        return UserProfile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # Ensure user profile exists and update it
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Save Profile on Login API (POST save profile)
class UserProfileSaveView(generics.CreateAPIView):
    """
    Save user profile details when the user logs in.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Save the user's profile after login
        serializer.save(user=self.request.user)
