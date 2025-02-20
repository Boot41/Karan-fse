import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Portfolio, Investment, UserProfile
from unittest.mock import patch
import pandas as pd

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass123')

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def portfolio(user):
    return Portfolio.objects.create(
        user=user,
        name="Test Portfolio",
        description="Test Description"
    )

@pytest.mark.django_db
class TestMarketDataViewSet:
    def test_get_stock_data_unauthenticated(self, api_client):
        url = reverse('api:market-data-get-stock-data')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_stock_data_no_symbol(self, authenticated_client):
        url = reverse('api:market-data-get-stock-data')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    @patch('yfinance.Ticker')
    def test_get_stock_data_success(self, mock_ticker, authenticated_client):
        # Mock the yfinance Ticker
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.info = {
            'longName': 'Apple Inc.',
            'currentPrice': 150.0,
            'currency': 'USD',
            'marketCap': 2500000000000,
            'trailingPE': 25.5,
            'dividendYield': 0.006
        }
        # Create a mock DataFrame for history
        mock_history = pd.DataFrame({
            'Open': [150.0],
            'High': [155.0],
            'Low': [149.0],
            'Close': [152.0],
            'Volume': [1000000]
        })
        mock_ticker_instance.history.return_value = mock_history

        url = reverse('api:market-data-get-stock-data')
        response = authenticated_client.get(f"{url}?symbol=AAPL")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['symbol'] == 'AAPL'
        assert response.data['company_name'] == 'Apple Inc.'
        assert response.data['current_price'] == 150.0

@pytest.mark.django_db
class TestPortfolioViewSet:
    def test_create_portfolio_unauthenticated(self, api_client):
        url = reverse('api:portfolio-list')
        response = api_client.post(url, {
            'name': 'Test Portfolio',
            'description': 'Test Description'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_portfolio_success(self, authenticated_client):
        url = reverse('api:portfolio-list')
        response = authenticated_client.post(url, {
            'name': 'Test Portfolio',
            'description': 'Test Description'
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Portfolio'

    def test_list_portfolios(self, authenticated_client, portfolio):
        url = reverse('api:portfolio-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == portfolio.name

@pytest.mark.django_db
class TestAIRecommendationViewSet:
    def test_get_recommendation_unauthenticated(self, api_client):
        url = reverse('api:ai-recommendation-get-recommendation')
        response = api_client.post(url, {
            'stock_symbol': 'AAPL',
            'investment_horizon': 'long_term',
            'risk_tolerance': 'moderate'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_recommendation_missing_params(self, authenticated_client):
        url = reverse('api:ai-recommendation-get-recommendation')
        response = authenticated_client.post(url, {
            'stock_symbol': 'AAPL'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data

    @patch('yfinance.Ticker')
    def test_get_recommendation_success(self, mock_ticker, authenticated_client):
        # Mock the yfinance Ticker
        mock_ticker_instance = mock_ticker.return_value
        mock_ticker_instance.info = {
            'currentPrice': 150.0,
            'trailingPE': 25.5,
            'marketCap': 2500000000000,
            'dividendYield': 0.006
        }
        # Create a mock DataFrame for history
        mock_history = pd.DataFrame({
            'Close': [150.0, 151.0, 152.0]
        })
        mock_ticker_instance.history.return_value = mock_history

        url = reverse('api:ai-recommendation-get-recommendation')
        response = authenticated_client.post(url, {
            'stock_symbol': 'AAPL',
            'investment_horizon': 'long_term',
            'risk_tolerance': 'moderate'
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['symbol'] == 'AAPL'
        assert 'recommendation' in response.data
        assert 'confidence_score' in response.data
