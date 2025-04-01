class PasswordBaseValidationError(Exception):
    """Base exception class for all password validation errors."""


class PasswordNotEqualError(Exception):
    """Raised when check password when password and confirm_password do not match."""


class PasswordShortLengthError(PasswordBaseValidationError):
    """Raised when validate password. Its length less than 8 characters."""


class PasswordNoDigitError(PasswordBaseValidationError):
    """Raised when validate password. He does not contain digit."""


class PasswordNoUpperAndLowerCharError(PasswordBaseValidationError):
    """Raise when validate pasword. He don't contrain upper and lowercase characters."""
