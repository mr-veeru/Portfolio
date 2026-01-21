"""
Custom Exception Classes
Application-specific exceptions for better error handling
"""

from typing import Optional


class ValidationError(Exception):
    """Raised when input validation fails"""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        super().__init__(message)
        self.message: str = message
        self.field: Optional[str] = field


class EmailServiceError(Exception):
    """Raised when email service fails"""

    def __init__(
        self, 
        message: str = 'Failed to send email', 
        original_error: Optional[Exception] = None
    ) -> None:
        super().__init__(message)
        self.message: str = message
        self.original_error: Optional[Exception] = original_error


class ConfigurationError(Exception):
    """Raised when configuration is invalid"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message: str = message

