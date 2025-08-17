National ID Validation Service

A Django-based service for validating Egyptian National IDs (NIDs) with API key authentication and quota management.

Features

Validate NIDs with century, governorate, gender, birth date, and check digit verification.

API Key authentication for rate-limited access.

Monthly quota management for API keys.

Redis caching for validated NIDs.

Admin interface to manage API keys and quotas.

Management command to reset quotas monthly.

Design Decisions

Custom APIKeyAuthentication middleware for key validation.

Luhn algorithm for check digit validation.

Redis cache to reduce repeated database lookups.

Separate APIKey model to track email, key, and quota.

Native Django tests for API key, NID validation, and views.

Dockerized setup for PostgreSQL, Redis, and Django.

Requirements

Python 3.11+, Django 5.2+, PostgreSQL, Redis

requirements.txt includes:

Django==5.2.5

djangorestframework

django-redis

psycopg2-binary

Running with Docker

Dockerfile builds the Django app image.

docker-compose.yml defines PostgreSQL, Redis, and Django services.

Start the app with:

docker-compose up --build


The service will be accessible at http://localhost:8000.

Superuser / Admin

Create a superuser to manage API keys and quotas:

docker-compose exec web python manage.py createsuperuser


Can create, view, delete API keys.

Can manually reset quotas or monitor usage.

Management Commands

Reset API Key Quotas
Run at the start of each month:

docker-compose exec web python manage.py reset_quotas


This refreshes API key quotas automatically.

Running Tests

Tests use native Django TestCase. Run them with:

docker-compose exec web python manage.py test

Notes

All validation requests require an X-API-Key header.

Validated NIDs are cached for 24 hours.

Monthly quotas prevent API abuse.

The last digit of NID is verified using the Luhn algorithm.

Endpoints
Method	  Endpoint	    Description	                                                        Auth Required
POST	  /validate/	    Validate a National ID. Returns validation result or error.	        No (X-API-Key required in production)
POST	  /api-keys/	    Create a new API key for an email. Returns hashed and unhashed key.	No (simplified for testing)
GET	    /api-keys/	    List all API keys.	                                                No (simplified for testing)
GET	    /api-keys/{id}/	Retrieve a specific API key by ID.	                                No (simplified for testing)
PUT	    /api-keys/{id}/	Update an API key record (email or quota).	                        No (simplified for testing)
PATCH	  /api-keys/{id}/	Partially update an API key.	                                      No (simplified for testing)
DELETE	/api-keys/{id}/	Delete an API key.	                                                No (simplified for testing)

Notes:

/validate/ is the main endpoint for NID validation and requires an X-API-Key header.

All APIKeyViewSet endpoints are exposed without authentication in this project for simplicity; in production, you should enable IsAdminUser for these actions.

Responses include the unhashed_key when creating a new API key so the user can see the actual key.

Environment Variables

DATABASE_URL: PostgreSQL connection string

DEBUG: Django debug mode

REDIS_URL: Redis connection string
