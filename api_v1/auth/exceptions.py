from exceptions import BaseLogicError, BaseValidationError


class UsernameOrEmailRequiredError(BaseValidationError):
    """Raised if username and email not specified during login."""


class UsernameValidationError(BaseValidationError):
    """Exception class for all username validation errors."""


class UsernameTooShortOrTooLongError(UsernameValidationError):
    """Raised when validate username. Its length less than 6 charachers."""


class InvalidUsernameCharacherError(UsernameValidationError):
    """Raised when validate username. Its contain only allowed characters."""


class PasswordValidationError(BaseValidationError):
    """Base exception class for all password validation errors."""


class PasswordShortLengthError(PasswordValidationError):
    """Raised when validate password. Its length less than 8 characters."""


class PasswordNoDigitError(PasswordValidationError):
    """Raised when validate password. He does not contain digit."""


class PasswordNoUpperAndLowerCharError(PasswordValidationError):
    """Raised when validate password. He don't contrain upper and lowercase char."""


class NoWhitespaceInPasswordError(PasswordValidationError):
    """Raised when password contains a space."""


class PasswordsNotEqualError(PasswordValidationError):
    """Raised when check password when password and confirm password do not match."""


class PasswordHashError(BaseLogicError):
    """Raised when hash is created incorrectly."""


class PasswordHashingIsError(PasswordHashError):
    """Raised when argon2 raised error: HashingError."""
