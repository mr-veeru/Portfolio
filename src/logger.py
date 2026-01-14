"""
Logging Configuration

Centralized logging setup for the application.
"""

import logging
import os
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from flask import Flask

from src.config import Config


def _cleanup_old_logs(log_dir: Path, days_to_keep: int = 7) -> None:
    """
    Delete log files older than specified days.

    Args:
        log_dir: Directory containing log files
        days_to_keep: Number of days to keep logs (default: 7)
    """
    if not log_dir.exists():
        return

    current_time: float = time.time()
    days_in_seconds: float = days_to_keep * 24 * 60 * 60

    for log_file in log_dir.glob('*.log*'):
        try:
            file_age: float = current_time - os.path.getmtime(log_file)
            if file_age > days_in_seconds:
                log_file.unlink()
                logging.info(f"Deleted old log file: {log_file.name}")
        except (OSError, PermissionError) as error:
            logging.warning(f"Could not delete log file {log_file.name}: {error}")


def setup_logging(app: Flask) -> None:
    """
    Configure logging for the Flask application.

    Args:
        app: Flask application instance
    """
    # Set log level from config
    log_level: int = getattr(logging, Config.LOG_LEVEL, logging.INFO)
    app.logger.setLevel(log_level)

    # Remove default handler if in production
    if not app.debug:
        # Remove console handler in production
        app.logger.handlers.clear()

        # Create logs directory if it doesn't exist
        log_dir: Path = Path('logs')
        log_dir.mkdir(exist_ok=True)

        # Cleanup old log files (older than 7 days)
        _cleanup_old_logs(log_dir, days_to_keep=7)

        # File handler with rotation
        file_handler: RotatingFileHandler = RotatingFileHandler(
            'logs/portfolio.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(log_level)
        app.logger.addHandler(file_handler)
    else:
        # In development, use console handler with better formatting
        console_handler: logging.StreamHandler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        console_handler.setLevel(log_level)
        app.logger.addHandler(console_handler)

    # Set level for third-party loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('flask_limiter').setLevel(logging.WARNING)

    app.logger.info('Portfolio application logging configured')


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
