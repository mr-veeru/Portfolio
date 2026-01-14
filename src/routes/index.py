"""
Index Routes

Home page and health check endpoints for the portfolio website.
"""

from flask import Blueprint, jsonify

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    """
    Root endpoint to welcome the user to the portfolio website.

    Returns:
        JSON response with welcome message
    """
    return jsonify({'message': 'Welcome to the Portfolio website'}), 200


@index_bp.route('/health')
def health():
    """
    Health check endpoint to verify the application is running.

    Returns:
        JSON response with health status
    """
    return jsonify({
        'message': 'Health check successful',
        'status': 'healthy'
    }), 200