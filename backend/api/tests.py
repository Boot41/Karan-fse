from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from .models import AIAnalysis
from .serializers import AIAnalysisSerializer

class AIAnalysisTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create sample analysis
        self.analysis = AIAnalysis.objects.create(
            user=self.user,
            query="Test query",
            provider="GEMINI",
            response="Test response",
            summary="Test summary"
        )
        
        # API endpoints
        self.list_url = reverse('api:analysis-list')
        self.detail_url = reverse('api:analysis-detail', kwargs={'pk': self.analysis.pk})

    def test_create_analysis(self):
        """Test creating a new analysis"""
        with patch('google.generativeai.GenerativeModel') as mock_gemini, \
             patch('openai.OpenAI') as mock_gpt, \
             patch('anthropic.Anthropic') as mock_claude:
            
            # Mock Gemini response
            mock_gemini.return_value.generate_content.return_value.text = "Gemini response"
            
            # Mock GPT response
            mock_gpt_instance = MagicMock()
            mock_gpt_instance.chat.completions.create.return_value.choices = [
                MagicMock(message=MagicMock(content="GPT response"))
            ]
            mock_gpt.return_value = mock_gpt_instance
            
            # Mock Claude response
            mock_claude_instance = MagicMock()
            mock_claude_instance.messages.create.return_value.content = [
                MagicMock(text="Claude response")
            ]
            mock_claude.return_value = mock_claude_instance
            
            data = {'query': 'Test analysis query'}
            response = self.client.post(self.list_url, data)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(AIAnalysis.objects.count(), 4)  # Original + 3 new (one per provider)
            self.assertEqual(response.data['query'], 'Test analysis query')

    def test_list_analysis(self):
        """Test listing analyses"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_analysis(self):
        """Test retrieving a specific analysis"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['query'], 'Test query')

    def test_update_analysis(self):
        """Test updating an analysis"""
        data = {'query': 'Updated query'}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['query'], 'Updated query')

    def test_delete_analysis(self):
        """Test deleting an analysis"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AIAnalysis.objects.count(), 0)

    def test_unauthorized_access(self):
        """Test unauthorized access to API"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_analysis_model(self):
        """Test AIAnalysis model"""
        analysis = AIAnalysis.objects.get(id=self.analysis.id)
        self.assertEqual(str(analysis), f"GEMINI Analysis for {self.user.username}")
        self.assertEqual(analysis.query, "Test query")
        self.assertEqual(analysis.provider, "GEMINI")

    def test_analysis_serializer(self):
        """Test AIAnalysis serializer"""
        serializer = AIAnalysisSerializer(instance=self.analysis)
        self.assertEqual(serializer.data['query'], "Test query")
        self.assertEqual(serializer.data['provider'], "GEMINI")
        self.assertEqual(serializer.data['response'], "Test response")
