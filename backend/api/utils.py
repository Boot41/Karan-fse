from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from requests.exceptions import RequestException
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that provides more detailed error responses
    """
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, ValidationError):
            response = Response({
                'error': 'Validation Error',
                'detail': str(exc),
                'code': 'validation_error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif isinstance(exc, IntegrityError):
            response = Response({
                'error': 'Database Integrity Error',
                'detail': 'The operation could not be completed due to a database constraint.',
                'code': 'integrity_error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        elif isinstance(exc, RequestException):
            response = Response({
                'error': 'External API Error',
                'detail': 'Failed to fetch data from external service.',
                'code': 'external_api_error'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        else:
            logger.error(f"Unhandled exception: {exc}")
            response = Response({
                'error': 'Internal Server Error',
                'detail': 'An unexpected error occurred.',
                'code': 'internal_error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response

def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class RateLimitMixin:
    """
    Mixin to add rate limiting to views
    """
    rate_limit = '5/minute'
    rate_limit_key = None

    def get_rate_limit_key(self, request):
        if self.rate_limit_key:
            return self.rate_limit_key
        return f"{get_client_ip(request)}_{self.__class__.__name__}"

def validate_stock_symbol(symbol):
    """
    Validate stock symbol format
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError('Stock symbol is required and must be a string')
    if not symbol.isalpha():
        raise ValidationError('Stock symbol must contain only letters')
    if not 1 <= len(symbol) <= 5:
        raise ValidationError('Stock symbol must be between 1 and 5 characters')
    return symbol.upper()

def sanitize_input(data):
    """
    Sanitize user input to prevent XSS and other injection attacks
    """
    if isinstance(data, str):
        # Remove potentially dangerous HTML/JavaScript
        from html import escape
        return escape(data.strip())
    elif isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(i) for i in data]
    return data
