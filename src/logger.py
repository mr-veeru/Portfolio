"""
Logging Configuration

Centralized logging setup for the application.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from flask import Flask

from src.config import Config


def setup_logging(app: Flask) -> None:
    """
    Configure logging for the Flask application.

    In development mode, preserves Flask's default console output.
    In production mode, sets up file-based logging with rotation.

    Args:
        app: Flask application instance
    """
    # Only configure logging in production
    if not Config.DEBUG:
        log_level = getattr(logging, Config.LOG_LEVEL, logging.INFO)

        # Clear existing handlers and set log level
        app.logger.setLevel(log_level)
        app.logger.handlers.clear()

        # Create logs directory
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        # Configure rotating file handler (10MB per file, keep 10 backups)
        file_handler = RotatingFileHandler(
            log_dir / 'portfolio.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)

        # Suppress verbose third-party logs in production
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        logging.getLogger('flask_limiter').setLevel(logging.WARNING)

        app.logger.info('Logging configured for production')


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
