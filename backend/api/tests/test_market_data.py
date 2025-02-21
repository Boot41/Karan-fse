import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from unittest.mock import patch
from api.models import StockData, StockAlert

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def stock_data():
    return {
        'symbol': 'AAPL',
        'price': '150.00',
        'volume': '1000000',
        'change_percent': '2.5'
    }

@pytest.fixture
def alert_data():
    return {
        'stock_symbol': 'AAPL',
        'target_price': '160.00',
        'alert_type': 'ABOVE',
        'is_active': True
    }

@pytest.mark.django_db
class TestMarketData:
    @patch('api.views.yfinance.Ticker')
    def test_get_stock_data(self, mock_ticker, authenticated_client):
        mock_ticker.return_value.info = {
            'symbol': 'AAPL',
            'regularMarketPrice': 150.00,
            'regularMarketVolume': 1000000,
            'regularMarketChangePercent': 2.5
        }

        url = reverse('api:market-data-get-stock-data')
        response = authenticated_client.get(url, {'symbol': 'AAPL'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['symbol'] == 'AAPL'
        assert 'price' in response.data
        assert 'volume' in response.data

    def test_create_stock_alert(self, authenticated_client, alert_data):
        url = reverse('api:stock-alert-list')
        response = authenticated_client.post(url, alert_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['stock_symbol'] == alert_data['stock_symbol']
        assert response.data['target_price'] == alert_data['target_price']

    def test_list_stock_alerts(self, authenticated_client, alert_data):
        # Create an alert first
        StockAlert.objects.create(
            user=authenticated_client.user,
            **alert_data
        )

        url = reverse('api:stock-alert-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['stock_symbol'] == alert_data['stock_symbol']

    @patch('api.views.yfinance.Ticker')
    def test_historical_data(self, mock_ticker, authenticated_client):
        mock_ticker.return_value.history.return_value = {
            'Open': [150.0],
            'High': [155.0],
            'Low': [148.0],
            'Close': [152.0],
            'Volume': [1000000]
        }

        url = reverse('api:market-data-historical')
        response = authenticated_client.get(url, {
            'symbol': 'AAPL',
            'period': '1d'
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'historical_data' in response.data

    def test_delete_stock_alert(self, authenticated_client, alert_data):
        # Create an alert first
        alert = StockAlert.objects.create(
            user=authenticated_client.user,
            **alert_data
        )

        url = reverse('api:stock-alert-detail', kwargs={'pk': alert.id})
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert StockAlert.objects.count() == 0

@pytest.mark.django_db
class TestAIRecommendations:
    @patch('api.views.google.generativeai.GenerativeModel')
    def test_get_ai_recommendation(self, mock_ai_model, authenticated_client):
        mock_ai_model.return_value.generate_content.return_value.text = (
            "Based on the analysis, AAPL shows strong potential for growth..."
        )

        url = reverse('api:ai-recommendation')
        response = authenticated_client.post(url, {
            'stock_symbol': 'AAPL',
            'analysis_type': 'fundamental'
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'recommendation' in response.data
        assert isinstance(response.data['recommendation'], str)
        assert len(response.data['recommendation']) > 0

    def test_invalid_stock_symbol(self, authenticated_client):
        url = reverse('api:ai-recommendation')
        response = authenticated_client.post(url, {
            'stock_symbol': 'INVALID',
            'analysis_type': 'fundamental'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_analysis_type(self, authenticated_client):
        url = reverse('api:ai-recommendation')
        response = authenticated_client.post(url, {
            'stock_symbol': 'AAPL'
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
