"""
Application Configuration

Centralized configuration management for the portfolio application.
"""

import os


class Config:
    """
    Base configuration class for the Flask application.

    Attributes:
        SECRET_KEY: Secret key for session management
        DEBUG: Debug mode flag
        LOG_LEVEL: Logging level (INFO, DEBUG, WARNING, ERROR)
    """

    # Flask configuration
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = os.getenv('FLASK_ENV', 'development').lower() != 'production'

    # Logging configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO').upper()
