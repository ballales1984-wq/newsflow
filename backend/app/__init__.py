"""
NewsFlow Backend Application
==================================

Core package for the NewsFlow FastAPI backend, an intelligent news
aggregation and curation platform.

Main structure:
- api/: REST API endpoints (v1)
- core/: Configuration, database, security, core utilities
- models/: SQLAlchemy ORM models
- schemas/: Pydantic schemas for validation/serialization
- services/: Business logic, collectors, NLP, Celery tasks

The application supports both SQLite (development) and PostgreSQL (production),
uses FastAPI for the REST API, SQLAlchemy for ORM, and Celery for
asynchronous processing.
"""
