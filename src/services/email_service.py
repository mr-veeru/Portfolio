"""
Email Service
Business logic for sending emails
"""

import smtplib
from typing import Optional, Union, Any, Dict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from src.exceptions import EmailServiceError, ConfigurationError
from src.config import Config
from src.logger import get_logger

logger = get_logger(__name__)


class EmailService:
    """Service for sending emails via SMTP"""

    def _get_config_value(self, key: str, default: Optional[Any] = None) -> Any:
        """Get config value from Flask config or Config class"""
        if hasattr(self.config, 'get'):
            return self.config.get(key, getattr(Config, key, default))
        return getattr(self.config, key, getattr(Config, key, default))

    def __init__(self, config: Optional[Union[Dict[str, Any], type]] = None) -> None:
        """
        Initialize email service

        Args:
            config: Configuration object (Flask config dict or Config class)

        Raises:
            ConfigurationError: If email configuration is invalid
        """
        self.config: Union[Dict[str, Any], type] = config if config is not None else Config

    def send_contact_form_email(
        self,
        name: str,
        email: str,
        subject: str,
        message: str
    ) -> bool:
        """
        Send contact form submission email

        Args:
            name: Sender's name
            email: Sender's email
            subject: Email subject
            message: Email message body

        Returns:
            True if email sent successfully, False otherwise

        Raises:
            EmailServiceError: If email sending fails
            ConfigurationError: If email configuration is invalid
        """
        # Check if email config is valid
        smtp_server: str = self._get_config_value('SMTP_SERVER')
        smtp_port_raw: Any = self._get_config_value('SMTP_PORT')
        smtp_username: str = self._get_config_value('SMTP_USERNAME')
        smtp_password: str = self._get_config_value('SMTP_PASSWORD')
        recipient_email: str = self._get_config_value('RECIPIENT_EMAIL')

        if not recipient_email:
            raise ConfigurationError("Missing RECIPIENT_EMAIL (where messages should be delivered).")

        if not smtp_server:
            raise ConfigurationError("Missing SMTP_SERVER.")

        try:
            smtp_port: int = int(smtp_port_raw) if smtp_port_raw is not None else 0
        except (TypeError, ValueError) as port_error:
            raise ConfigurationError("Invalid SMTP_PORT. Must be an integer.") from port_error

        if not smtp_port:
            raise ConfigurationError("Missing SMTP_PORT.")

        if not (smtp_username and smtp_password):
            raise ConfigurationError(
                "Email service is not configured. Please set SMTP_USERNAME and SMTP_PASSWORD."
            )

        try:
            logger.info(f"Sending contact form email from {name} ({email})")
            # Create email message
            email_message: MIMEMultipart = self._create_message(name, email, subject, message)

            # Send email
            self._send_message(email_message)
            
            logger.info(f"Successfully sent contact form email from {name} ({email})")
            return True

        except smtplib.SMTPException as smtp_error:
            error_message: str = f"SMTP error while sending email: {str(smtp_error)}"
            logger.error(f"SMTP error: {error_message}", exc_info=True)
            raise EmailServiceError(error_message, original_error=smtp_error)

        except Exception as unexpected_error:
            error_message: str = f"Unexpected error while sending email: {str(unexpected_error)}"
            logger.error(f"Unexpected error sending email: {error_message}", exc_info=True)
            raise EmailServiceError(error_message, original_error=unexpected_error)

    def _create_message(
        self,
        name: str,
        email: str,
        subject: str,
        message: str
    ) -> MIMEMultipart:
        """
        Create email message

        Args:
            name: Sender's name
            email: Sender's email
            subject: Email subject
            message: Email message body

        Returns:
            MIMEMultipart message object
        """
        smtp_username: str = self._get_config_value('SMTP_USERNAME')
        recipient_email: str = self._get_config_value('RECIPIENT_EMAIL')

        if not recipient_email:
            raise ConfigurationError("Missing RECIPIENT_EMAIL (where messages should be delivered).")

        email_message: MIMEMultipart = MIMEMultipart()
        email_message['From'] = smtp_username
        email_message['To'] = recipient_email
        email_message['Subject'] = f"Portfolio Contact: {subject}"
        email_message['Reply-To'] = email

        # Create email body
        email_body: str = f"""New contact form submission from your portfolio:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
Sent from portfolio contact form at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        email_message.attach(MIMEText(email_body, 'plain'))

        return email_message

    def _send_message(self, email_message: MIMEMultipart) -> None:
        """
        Send email message via SMTP

        Args:
            email_message: MIMEMultipart message object

        Raises:
            EmailServiceError: If sending fails
        """
        smtp_server: str = self._get_config_value('SMTP_SERVER')
        smtp_port_raw: Any = self._get_config_value('SMTP_PORT')
        smtp_username: str = self._get_config_value('SMTP_USERNAME')
        smtp_password: str = self._get_config_value('SMTP_PASSWORD')

        if not smtp_server:
            raise ConfigurationError("Missing SMTP_SERVER.")

        try:
            smtp_port: int = int(smtp_port_raw) if smtp_port_raw is not None else 0
        except (TypeError, ValueError) as port_error:
            raise ConfigurationError("Invalid SMTP_PORT. Must be an integer.") from port_error

        if not smtp_port:
            raise ConfigurationError("Missing SMTP_PORT.")

        try:
            logger.debug(f"Connecting to SMTP server {smtp_server}:{smtp_port}")
            # Add timeout to prevent hanging (10 seconds for connection, 30 seconds total)
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as smtp_server_connection:
                # Always enforce TLS
                smtp_server_connection.starttls()
                smtp_server_connection.login(smtp_username, smtp_password)
                smtp_server_connection.send_message(email_message)
            logger.debug("Email sent successfully via SMTP")

        except smtplib.SMTPAuthenticationError as auth_error:
            logger.error(f"SMTP authentication failed for {smtp_username}")
            raise EmailServiceError(
                "SMTP authentication failed. Please check your credentials.",
                original_error=auth_error
            )
        except (smtplib.SMTPConnectError, OSError, TimeoutError) as connection_error:
            logger.error(f"Failed to connect to SMTP server {smtp_server}:{smtp_port} - {str(connection_error)}")
            # Check if this might be a port blocking issue (common on free hosting tiers)
            if "Connection refused" in str(connection_error) or "timed out" in str(connection_error).lower():
                raise EmailServiceError(
                    f"Unable to connect to SMTP server. This may be due to port blocking on your hosting provider. "
                    f"Please check your SMTP configuration or consider using an HTTP-based email service.",
                    original_error=connection_error
                )
            raise EmailServiceError(
                f"Failed to connect to SMTP server {smtp_server}:{smtp_port}",
                original_error=connection_error
            )
        except smtplib.SMTPException as smtp_error:
            logger.error(f"SMTP error: {str(smtp_error)}")
            raise EmailServiceError(
                f"SMTP error: {str(smtp_error)}",
                original_error=smtp_error
            )

