# National ID Validation Service

A Django-based service for validating Egyptian National IDs (NIDs) with API key authentication and quota management.

## Features

- Validate NIDs with century, governorate, gender, birth date, and check digit verification.
- API Key authentication for rate-limited access.
- Monthly quota management for API keys.
- Redis caching for validated NIDs.
- Admin interface to manage API keys and quotas.
- Management command to reset quotas monthly.

## Design Decisions

- Custom `APIKeyAuthentication` middleware for key validation.
- Luhn algorithm for check digit validation.
- Redis cache to reduce repeated database lookups.
- Separate `APIKey` model to track email, key, and quota.
- Native Django tests for API key, NID validation, and views.
- Dockerized setup for PostgreSQL, Redis, and Django.

## Requirements

- Python 3.11+
- Django 5.2+
- PostgreSQL
- Redis
