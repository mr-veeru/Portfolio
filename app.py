"""
Portfolio Website - Main Application File

This module contains the Flask application setup and routing for the portfolio website.
"""

from flask import Flask


def create_app() -> Flask:
    """
    Create and configure the Flask application instance.

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    return app


# Initialize the Flask application
app = create_app()


@app.route('/')
def index():
    """
    Home page route handler.

    Returns:
        str: Welcome message for the portfolio website
    """
    return 'Hello, World!'


if __name__ == '__main__':
    # Run the application in debug mode for development
    app.run(debug=True)