"""
Application Configuration

Centralized configuration management for the portfolio application.
"""

import os


class Config:
    """
    Base configuration class for the Flask application.

    This class manages all application configuration settings including
    Flask-specific settings and logging configuration. Values are loaded
    from environment variables with sensible defaults for development.

    Attributes:
        SECRET_KEY: Secret key for session management and CSRF protection
        DEBUG: Debug mode flag (True for development, False for production)
        LOG_LEVEL: Logging level (INFO, DEBUG, WARNING, ERROR)
    """

    # Flask Configuration
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = os.getenv('FLASK_ENV', 'development').lower() != 'production'

    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO').upper()
