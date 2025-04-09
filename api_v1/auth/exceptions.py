from exceptions import BaseLogicError, BaseValidationError


class ProfileValidationError(BaseValidationError):
    """Base profile validation exception."""


class DateOfBirthMinAgeError(ProfileValidationError):
    """Raised when date of birth is less than allow age."""


class DateOfBirthFutureError(ProfileValidationError):
    """Raised when date of birth in future."""


class ProfileNameOrSurnameInvalidCharacherError(ProfileValidationError):
    """Raised when profile name or surname contain incorrect char."""


class ProfileNameOrSurnameNoWhitespaceError(ProfileValidationError):
    """Raised when profile name or surname contain whitespace."""


class UsernameOrEmailRequiredError(BaseValidationError):
    """Raised if username and email not specified during login."""


class UsernameValidationError(BaseValidationError):
    """Exception class for all username validation errors."""


class InvalidUsernameCharacherError(UsernameValidationError):
    """Raised when validate username. Its contain only allowed characters."""


class PasswordValidationError(BaseValidationError):
    """Base exception class for all password validation errors."""


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
