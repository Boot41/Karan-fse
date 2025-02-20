# AI Investment Platform Backend

A Django-based backend for an AI-powered investment advisory platform that provides stock market analysis, portfolio management, and AI-powered investment recommendations.

## Features

- JWT Authentication
- Real-time stock data using WebSockets
- AI-powered investment recommendations
- Portfolio management
- Email verification
- Rate limiting
- Caching with Redis
- Comprehensive test coverage
- API documentation with Swagger/OpenAPI

## Prerequisites

- Python 3.10+
- PostgreSQL
- Redis
- Virtual environment

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp backend/.env.template backend/.env
```
Edit the .env file with your configurations.

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

## Development Server

```bash
python manage.py runserver
```

## Production Deployment

1. Update production settings:
```bash
cp backend/.env.template backend/.env.prod
```
Edit the .env.prod file with production configurations.

2. Set environment variable:
```bash
export DJANGO_SETTINGS_MODULE=backend.settings_prod
```

3. Install production dependencies:
```bash
pip install gunicorn uvicorn
```

4. Collect static files:
```bash
python manage.py collectstatic --noinput
```

5. Run with gunicorn:
```bash
gunicorn -c gunicorn_config.py backend.asgi:application
```

## API Documentation

API documentation is available at:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## Testing

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
coverage run -m pytest
coverage report
```

## Security Features

- JWT Authentication
- Rate limiting
- Input validation
- XSS protection
- CSRF protection
- Secure cookie configuration
- CORS configuration
- Password validation rules

## Caching

Redis is used for caching:
- Stock data (5 minutes)
- API responses (configurable)
- Session data
- Rate limiting data

## WebSocket Endpoints

- `/ws/stock/<symbol>/`: Real-time stock updates
- `/ws/portfolio/<portfolio_id>/`: Real-time portfolio updates

## Environment Variables

Required environment variables:
- Database configuration
- Redis configuration
- Email settings
- API keys (Alpha Vantage, Finnhub, Google)
- JWT settings
- Production host settings

## Maintenance

1. Monitor logs:
```bash
tail -f logs/django.log
```

2. Backup database:
```bash
python manage.py dumpdata > backup.json
```

3. Clear cache:
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)
