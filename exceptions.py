class BaseExceptionError(Exception):
    """Base exception for all users errors in project."""


class BaseSystemError(BaseExceptionError):
    """Exception related system failures."""


class BaseExternalError(BaseExceptionError):
    """Exception related to external services."""


class BaseInfraError(BaseExceptionError):
    """Exception related to infrastructure components."""


class BaseLogicError(BaseExceptionError):
    """Exception related errors in business logic of application."""


class BaseValidationError(BaseExceptionError):
    """Exception related input validation errors."""
