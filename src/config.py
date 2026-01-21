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

    # Contact Form Validation
    MAX_NAME_LENGTH: int = int(os.getenv('MAX_NAME_LENGTH', '100'))
    MAX_EMAIL_LENGTH: int = int(os.getenv('MAX_EMAIL_LENGTH', '254'))
    MAX_SUBJECT_LENGTH: int = int(os.getenv('MAX_SUBJECT_LENGTH', '200'))
    MAX_MESSAGE_LENGTH: int = int(os.getenv('MAX_MESSAGE_LENGTH', '5000'))

    # Email / SMTP Configuration
    # Note: Many hosting providers block SMTP ports; consider an HTTP-based email provider if needed.
    SMTP_SERVER: str = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT: int = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME: str = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD: str = os.getenv('SMTP_PASSWORD', '')
    RECIPIENT_EMAIL: str = os.getenv('RECIPIENT_EMAIL', 'mr.veeru68@gmail.com')

    @classmethod
    def validate_email_config(cls) -> bool:
        """
        Validate that minimum email configuration is present.

        Returns:
            True if email configuration is sufficient to attempt sending.
        """
        if not cls.RECIPIENT_EMAIL:
            return False

        if not cls.SMTP_SERVER or not cls.SMTP_PORT:
            return False

        if not cls.SMTP_USERNAME or not cls.SMTP_PASSWORD:
            return False

        return True
