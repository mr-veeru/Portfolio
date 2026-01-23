"""
Portfolio Website - Main Application File

This module contains the Flask application setup and routing for the portfolio website.
"""

from flask import Flask
from dotenv import load_dotenv

from src.config import Config
from src.logger import setup_logging
from src.routes.index import index_bp
from src.routes.contact import contact_bp
from src.routes.api import api_bp
from src.extensions import limiter

# Load environment variables from .env file
load_dotenv()

def create_app() -> Flask:
    """
    Create and configure the Flask application instance.

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize rate limiter
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(api_bp)

    # Setup logging (only in production)
    if not Config.DEBUG:
        setup_logging(app)

    return app


# Initialize the Flask application
app = create_app()


if __name__ == '__main__':
    # Run the application in debug mode for development
    app.run(debug=Config.DEBUG)
