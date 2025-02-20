from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, PortfolioSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Portfolio, AIRecommendation
import yfinance as yf
import openai
import json
from datetime import datetime
from rest_framework.exceptions import APIException, ValidationError
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class StockDataError(APIException):
    status_code = 503
    default_detail = 'Error fetching stock data'
    default_code = 'stock_data_error'

# Dummy user for PoC
DEMO_USER_ID = 1

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user with their investment profile
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def portfolio_list(request):
    """
    List all portfolios or create a new portfolio
    """
    if request.method == 'GET':
        portfolios = Portfolio.objects.filter(user=request.user)
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PortfolioSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def portfolio_detail(request, pk):
    """
    Retrieve, update or delete a portfolio
    """
    try:
        portfolio = Portfolio.objects.get(pk=pk, user=request.user)
    except Portfolio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PortfolioSerializer(portfolio, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_investment_recommendation(request):
    """
    Get AI-powered investment recommendations based on user query
    """
    try:
        query = request.data.get('query', '')
        risk_profile = request.data.get('risk_profile', 'moderate')
        investment_horizon = request.data.get('investment_horizon', 'medium-term')

        # Get market data for popular stocks
        stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
        market_data = {}
        for stock in stocks:
            ticker = yf.Ticker(stock)
            info = ticker.info
            market_data[stock] = {
                'current_price': info.get('currentPrice', 0),
                'pe_ratio': info.get('forwardPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
            }

        # Prepare prompt for LLM
        prompt = f"""
        As an AI investment advisor, provide recommendations based on:
        User Query: {query}
        Risk Profile: {risk_profile}
        Investment Horizon: {investment_horizon}
        
        Current Market Data:
        {json.dumps(market_data, indent=2)}
        
        Provide specific investment recommendations including:
        1. Recommended stocks
        2. Reasoning behind each recommendation
        3. Risk assessment
        4. Investment timeline suggestions
        """

        # Get AI recommendation
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert investment advisor."},
                {"role": "user", "content": prompt}
            ]
        )

        recommendation = response.choices[0].message.content

        # Store recommendation in database
        AIRecommendation.objects.create(
            user_id=request.user.id,
            stock_symbol="MULTIPLE",
            recommendation_type="custom",
            confidence_score=85,
            reasoning=recommendation
        )

        return Response({
            'recommendation': recommendation,
            'market_data': market_data
        })

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_market_analysis(request):
    """
    Get real-time market analysis and trends
    """
    try:
        # Get market data for major indices and stocks
        symbols = {
            'indices': ['^GSPC', '^DJI', '^IXIC'],  # S&P 500, Dow Jones, NASDAQ
            'stocks': ['AAPL', 'GOOGL', 'MSFT', 'AMZN']  # Major tech stocks
        }
        
        market_analysis = {
            'indices': {},
            'stocks': {},
            'market_summary': {}
        }
        
        # Get indices data
        for index in symbols['indices']:
            try:
                ticker = yf.Ticker(index)
                current_data = ticker.history(period="1d")
                if not current_data.empty:
                    market_analysis['indices'][index] = {
                        'current_price': float(current_data['Close'].iloc[-1]),
                        'daily_change': float(current_data['Close'].iloc[-1] - current_data['Open'].iloc[0]),
                        'volume': float(current_data['Volume'].iloc[-1]) if 'Volume' in current_data else 0
                    }
            except Exception as e:
                market_analysis['indices'][index] = {'error': str(e)}

        # Get stocks data
        for stock in symbols['stocks']:
            try:
                ticker = yf.Ticker(stock)
                info = ticker.info
                market_analysis['stocks'][stock] = {
                    'current_price': info.get('currentPrice', 0),
                    'company_name': info.get('longName', ''),
                    'market_cap': info.get('marketCap', 0),
                    'pe_ratio': info.get('forwardPE', 0)
                }
            except Exception as e:
                market_analysis['stocks'][stock] = {'error': str(e)}

        # Add market summary
        market_analysis['market_summary'] = {
            'timestamp': str(datetime.now()),
            'total_stocks_analyzed': len(symbols['stocks']),
            'total_indices_analyzed': len(symbols['indices'])
        }

        return Response(market_analysis)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_portfolio(request):
    """
    Analyze existing portfolio and provide optimization suggestions
    """
    try:
        portfolio_data = request.data.get('portfolio', [])
        risk_tolerance = request.data.get('risk_tolerance', 'moderate')

        # Analyze portfolio performance
        total_value = 0
        portfolio_analysis = []

        for item in portfolio_data:
            ticker = yf.Ticker(item['symbol'])
            info = ticker.info
            current_price = info.get('currentPrice', 0)
            value = current_price * item['quantity']
            total_value += value

            portfolio_analysis.append({
                'symbol': item['symbol'],
                'current_value': value,
                'performance': ((current_price - item['purchase_price']) / item['purchase_price']) * 100
            })

        # Get AI-powered portfolio suggestions
        prompt = f"""
        Analyze this investment portfolio:
        Portfolio Details: {json.dumps(portfolio_analysis, indent=2)}
        Risk Tolerance: {risk_tolerance}
        Total Portfolio Value: ${total_value:,.2f}

        Provide:
        1. Portfolio performance analysis
        2. Diversification recommendations
        3. Rebalancing suggestions
        4. Risk management advice
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert portfolio manager."},
                {"role": "user", "content": prompt}
            ]
        )

        return Response({
            'portfolio_analysis': portfolio_analysis,
            'total_value': total_value,
            'ai_recommendations': response.choices[0].message.content
        })

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import yfinance as yf
import requests
from datetime import datetime, timedelta
import google.generativeai as genai
from decimal import Decimal
import asyncio
import aiohttp

from .models import (
    UserProfile, Portfolio, Investment,
    StockData, AIRecommendation
)
from .serializers import (
    UserProfileSerializer, PortfolioSerializer,
    InvestmentSerializer, StockDataSerializer,
    AIRecommendationSerializer
)

# Configure Gemini AI
genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class MarketDataViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def get_stock_data(self, request):
        symbol = request.query_params.get('symbol')
        
        if not symbol:
            return Response(
                {'error': 'Stock symbol is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            history = ticker.history(period='1d')
            
            if not info:
                return Response(
                    {'error': f'No data found for symbol {symbol}'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            data = {
                'symbol': symbol,
                'company_name': info.get('longName'),
                'current_price': info.get('currentPrice'),
                'currency': info.get('currency'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('trailingPE'),
                'dividend_yield': info.get('dividendYield'),
                'daily_data': {
                    'open': history['Open'].iloc[-1] if not history.empty else None,
                    'high': history['High'].iloc[-1] if not history.empty else None,
                    'low': history['Low'].iloc[-1] if not history.empty else None,
                    'close': history['Close'].iloc[-1] if not history.empty else None,
                    'volume': history['Volume'].iloc[-1] if not history.empty else None
                }
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Unexpected error for symbol {symbol}: {e}")
            return Response(
                {'error': 'Failed to fetch stock data'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PortfolioViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortfolioSerializer
    
    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InvestmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvestmentSerializer
    
    def get_queryset(self):
        return Investment.objects.filter(portfolio__user=self.request.user)

class AIRecommendationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_recommendation(self, request):
        try:
            data = request.data
            symbol = data.get('stock_symbol', '').upper()
            investment_horizon = data.get('investment_horizon', '')
            risk_tolerance = data.get('risk_tolerance', '')

            if not all([symbol, investment_horizon, risk_tolerance]):
                raise ValidationError({
                    'error': 'stock_symbol, investment_horizon, and risk_tolerance are required'
                })

            # Try to get stock data
            stock = yf.Ticker(symbol)
            info = stock.info

            # Get historical data
            hist = stock.history(period="1y")

            # Format data for AI analysis
            stock_data = {
                'current_price': info.get('currentPrice', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'market_cap': info.get('marketCap', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'historical_volatility': hist['Close'].pct_change().std() * (252 ** 0.5)
            }

            # Generate AI recommendation
            recommendation = self.generate_ai_recommendation(
                symbol, 
                stock_data, 
                investment_horizon, 
                risk_tolerance
            )

            return Response(recommendation)

        except ValidationError as e:
            raise e
        except Exception as e:
            logger.error(f"Error generating recommendation for {symbol}: {str(e)}")
            raise APIException(detail='Failed to generate recommendation')

    def generate_ai_recommendation(self, symbol, stock_data, horizon, risk):
        # Implementation of AI recommendation logic
        # This is a placeholder - implement actual AI logic
        return {
            'symbol': symbol,
            'recommendation': 'buy',  # or 'sell' or 'hold'
            'confidence_score': 0.85,
            'analysis': {
                'technical': {
                    'trend': 'upward',
                    'strength': 'strong'
                },
                'fundamental': {
                    'pe_ratio_analysis': 'favorable',
                    'market_cap_category': 'large_cap'
                }
            },
            'risk_assessment': 'moderate',
            'target_price': stock_data['current_price'] * 1.15,
            'stop_loss': stock_data['current_price'] * 0.90
        }
