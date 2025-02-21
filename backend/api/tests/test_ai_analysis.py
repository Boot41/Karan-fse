import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from api.models import AIAnalysis
from unittest.mock import patch

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

@pytest.mark.django_db
class TestAIAnalysis:
    def test_create_analysis(self, authenticated_client):
        url = reverse('api:analysis-list')
        data = {
            'query': 'What are the key features of Python?',
            'provider': 'GEMINI'
        }
        
        with patch('google.generativeai.GenerativeModel') as mock_gemini, \
             patch('openai.OpenAI') as mock_openai, \
             patch('anthropic.Anthropic') as mock_anthropic:
            
            # Mock responses
            mock_gemini.return_value.generate_content.return_value.text = "Gemini response"
            mock_openai.return_value.chat.completions.create.return_value.choices = [
                type('Choice', (), {'message': type('Message', (), {'content': "GPT response"})})()
            ]
            mock_anthropic.return_value.messages.create.return_value.content = [
                type('Content', (), {'text': "Claude response"})()
            ]
            
            response = authenticated_client.post(url, data)
            
        assert response.status_code == status.HTTP_201_CREATED
        assert AIAnalysis.objects.count() == 3  # One for each provider
        assert response.data['query'] == data['query']

    def test_list_analysis(self, authenticated_client, user):
        # Create some test analyses
        AIAnalysis.objects.create(
            user=user,
            query='Test query',
            provider='GEMINI',
            response='Test response',
            summary='Test summary'
        )
        
        url = reverse('api:analysis-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['query'] == 'Test query'

    def test_unauthorized_access(self, api_client):
        url = reverse('api:analysis-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
