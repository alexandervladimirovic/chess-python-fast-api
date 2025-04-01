# Username Validation
class UsernameBaseValidationError(Exception):
    """Base exception class for all username validation errors."""


class UsernameTooShortError(UsernameBaseValidationError):
    """Raised when validate username. Its length less than 6 charachers."""


class InvalidUsernameCharacherError(UsernameBaseValidationError):
    """Raised when validate username. Its contain only allowed characters."""


# Password Validation
class PasswordBaseValidationError(Exception):
    """Base exception class for all password validation errors."""


class PasswordShortLengthError(PasswordBaseValidationError):
    """Raised when validate password. Its length less than 8 characters."""


class PasswordNoDigitError(PasswordBaseValidationError):
    """Raised when validate password. He does not contain digit."""


class PasswordNoUpperAndLowerCharError(PasswordBaseValidationError):
    """Raised when validate password. He don't contrain upper and lowercase char."""


class NoWhitespaceInPasswordError(PasswordBaseValidationError):
    """Raised when password contains a space."""


# Password and confirm_password not equal
class PasswordNotEqualError(Exception):
    """Raised when check password when password and confirm_password do not match."""


# Username or email is transmitted during login.
class UsernameOrEmailRequiredError(Exception):
    """Raised if username and email not specified during login."""
