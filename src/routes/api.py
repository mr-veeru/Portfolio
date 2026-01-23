"""
Portfolio API Routes
RESTful API endpoints for portfolio data
"""

from typing import Callable, Any, Tuple
from flask import Blueprint, jsonify, Response
from src.data.data import Data
from src.logger import get_logger

logger = get_logger(__name__)

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


def _handle_api_request(
    service_method: Callable[[], Any],
    resource_name: str,
    include_count: bool = True
) -> Tuple[Response, int]:
    """
    Generic handler for API requests to reduce code duplication.

    Args:
        service_method: Service method to call
        resource_name: Name of the resource for logging/error messages
        include_count: Whether to include count in response

    Returns:
        Tuple of (JSON response, HTTP status code)
    """
    try:
        data = service_method()
        if include_count:
            logger.debug(f"Returning {len(data)} {resource_name}")
            return jsonify({
                'success': True,
                'data': data,
                'count': len(data)
            }), 200
        else:
            logger.debug(f"Returning {resource_name}")
            return jsonify({
                'success': True,
                'data': data
            }), 200
    except Exception as e:
        logger.error(f"Error fetching {resource_name}: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Failed to fetch {resource_name}'
        }), 500


@api_bp.route('/projects', methods=['GET'])
def get_projects() -> Tuple[Response, int]:
    """Get all projects"""
    return _handle_api_request(
        Data.get_projects,
        'projects'
    )


@api_bp.route('/skills', methods=['GET'])
def get_skills() -> Tuple[Response, int]:
    """Get all skills organized by category"""
    return _handle_api_request(
        Data.get_skills,
        'skill categories'
    )


@api_bp.route('/experience', methods=['GET'])
def get_experience() -> Tuple[Response, int]:
    """Get all experience items"""
    return _handle_api_request(
        Data.get_experience,
        'experience items'
    )


@api_bp.route('/education', methods=['GET'])
def get_education() -> Tuple[Response, int]:
    """Get all education items"""
    return _handle_api_request(
        Data.get_education,
        'education items'
    )


@api_bp.route('/certifications', methods=['GET'])
def get_certifications() -> Tuple[Response, int]:
    """Get all certifications"""
    return _handle_api_request(
        Data.get_certifications,
        'certifications'
    )


@api_bp.route('/stats', methods=['GET'])
def get_stats() -> Tuple[Response, int]:
    """Get portfolio statistics"""
    return _handle_api_request(
        Data.get_stats,
        'portfolio statistics',
        include_count=False
    )
