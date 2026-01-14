"""
Portfolio Website - Main Application File

This module contains the Flask application setup and routing for the portfolio website.
"""

from flask import Flask

from src.config import Config
from src.logger import setup_logging
from src.routes.index import index_bp


def create_app() -> Flask:
    """
    Create and configure the Flask application instance.

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(index_bp)

    # Setup logging (only in production)
    if not Config.DEBUG:
        setup_logging(app)

    return app


# Initialize the Flask application
app = create_app()


if __name__ == '__main__':
    # Run the application in debug mode for development
    app.run(debug=True)