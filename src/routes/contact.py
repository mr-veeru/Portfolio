"""
Contact Form Routes
Handle contact form submissions
"""

from typing import Tuple
from flask import Blueprint, request, jsonify, current_app, Response
from email_validator import validate_email, EmailNotValidError
from src.config import Config
from src.logger import get_logger
from src.exceptions import ValidationError
from src.services.email_service import EmailService
from src.extensions import limiter

logger = get_logger(__name__)


# Create blueprint
contact_bp = Blueprint('contact', __name__)


@contact_bp.route('/contact', methods=['POST'])
@limiter.limit(Config.RATE_LIMIT_DEFAULTS)
def submit_contact_form() -> Tuple[Response, int]:
    """Handle contact form submissions via AJAX"""
    client_ip: str = request.remote_addr or 'unknown'
    logger.info(f"Contact form submission attempt from IP: {client_ip}")

    try:
        # Get and validate form data
        name: str = request.form.get('name', '').strip()
        email: str = request.form.get('email', '').strip()
        subject: str = request.form.get('subject', '').strip()
        message: str = request.form.get('message', '').strip()

        # Validate required fields
        for field_name, field_value in [('name', name), ('email', email), ('subject', subject), ('message', message)]:
            if not field_value:
                raise ValidationError(f'{field_name.capitalize()} is required and cannot be empty', field=field_name)

        # Validate lengths
        if len(name) > Config.MAX_NAME_LENGTH:
            raise ValidationError(f'Name is too long (maximum {Config.MAX_NAME_LENGTH} characters)', field='name')
        if len(email) > Config.MAX_EMAIL_LENGTH:
            raise ValidationError(f'Email is too long (maximum {Config.MAX_EMAIL_LENGTH} characters)', field='email')
        if len(subject) > Config.MAX_SUBJECT_LENGTH:
            raise ValidationError(f'Subject is too long (maximum {Config.MAX_SUBJECT_LENGTH} characters)', field='subject')
        if len(message) > Config.MAX_MESSAGE_LENGTH:
            raise ValidationError(f'Message is too long (maximum {Config.MAX_MESSAGE_LENGTH} characters)', field='message')

        # Validate and normalize email
        try:
            email_validation_info = validate_email(email, check_deliverability=False)
            email = email_validation_info.normalized
        except EmailNotValidError as validation_error:
            raise ValidationError(
                f'Invalid email address: {str(validation_error)}',
                field='email'
            )

        # Check if email is configured before attempting to send
        if not Config.validate_email_config():
            logger.warning(f"Email not configured - contact form submission from {name} ({email}) cannot be sent")
            return jsonify({
                'success': False,
                'message': 'Email service is not configured. Please contact me directly via email.'
            }), 503  # Service Unavailable

        # Send email
        email_service: EmailService = EmailService(current_app.config)
        try:
            email_service.send_contact_form_email(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            logger.info(f"Contact form submitted successfully from {name} ({email})")
            return jsonify({
                'success': True,
                'message': 'Message sent successfully! I\'ll get back to you soon.'
            }), 200
        except Exception as email_error:
            # Catch email-specific errors and return user-friendly message
            logger.error(f"Email sending failed for contact form from {name} ({email}): {str(email_error)}")
            recipient_email: str = Config.RECIPIENT_EMAIL
            return jsonify({
                'success': False,
                'message': f'Unable to send email at this time. Please contact me directly at {recipient_email}'
            }), 503  # Service Unavailable

    except ValidationError as e:
        logger.warning(f"Validation error in contact form from IP {client_ip}: {e.message}")
        return jsonify({
            'success': False,
            'message': f'Error: {e.message}'
        }), 400
    except Exception as e:
        logger.error(f"Unexpected error processing contact form from IP {client_ip}: {str(e)}", exc_info=True)
        recipient_email: str = Config.RECIPIENT_EMAIL
        return jsonify({
            'success': False,
            'message': f'An error occurred. Please try again or email me directly at {recipient_email}'
        }), 500
