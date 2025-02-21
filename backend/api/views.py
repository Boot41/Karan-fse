from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from datetime import datetime, timedelta
from .models import (
    UserProfile, Portfolio, Investment, 
    StockAlert, AIRecommendation, StockData, AIAnalysis
)
from .serializers import (
    UserProfileSerializer, PortfolioSerializer,
    InvestmentSerializer, StockAlertSerializer,
    AIRecommendationSerializer, StockDataSerializer, AIAnalysisSerializer
)
from .services.financial_service import FinancialService

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PortfolioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def analyze(self, request, pk=None):
        """
        Get AI-powered analysis for the entire portfolio
        """
        portfolio = self.get_object()
        financial_service = FinancialService()
        analysis = financial_service.get_portfolio_analysis(portfolio)
        
        if analysis:
            return Response(analysis)
        return Response(
            {"error": "Could not generate portfolio analysis"},
            status=status.HTTP_400_BAD_REQUEST
        )

class InvestmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InvestmentSerializer

    def get_queryset(self):
        return Investment.objects.filter(portfolio__user=self.request.user)

    @action(detail=True, methods=['get'])
    def analysis(self, request, pk=None):
        """
        Get detailed analysis for an investment
        """
        investment = self.get_object()
        financial_service = FinancialService()
        
        # Get current stock data
        stock_data = financial_service.get_stock_data(investment.symbol)
        if not stock_data:
            return Response(
                {"error": "Could not fetch stock data"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get user profile for personalized recommendations
        user_profile = UserProfile.objects.get(user=request.user)
        
        # Generate AI recommendation
        recommendation = financial_service.generate_ai_recommendation(
            user_profile,
            investment.symbol
        )

        if recommendation:
            return Response({
                "stock_data": stock_data,
                "recommendation": AIRecommendationSerializer(recommendation).data
            })
        return Response(
            {"error": "Could not generate recommendation"},
            status=status.HTTP_400_BAD_REQUEST
        )

class StockAlertViewSet(viewsets.ModelViewSet):
    """ViewSet for managing stock price alerts"""
    serializer_class = StockAlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StockAlert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AIRecommendationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIRecommendation.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def get_recommendation(self, request):
        """
        Get AI-powered investment recommendation
        """
        symbol = request.data.get('symbol')
        if not symbol:
            return Response(
                {"error": "Symbol is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        financial_service = FinancialService()
        user_profile = UserProfile.objects.get(user=request.user)
        
        recommendation = financial_service.generate_ai_recommendation(
            user_profile,
            symbol
        )

        if recommendation:
            return Response(AIRecommendationSerializer(recommendation).data)
        return Response(
            {"error": "Could not generate recommendation"},
            status=status.HTTP_400_BAD_REQUEST
        )

class AIAnalysisViewSet(viewsets.ModelViewSet):
    """ViewSet for handling AI analysis using multiple LLM providers"""
    serializer_class = AIAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIAnalysis.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
