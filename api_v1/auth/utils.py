from argon2.exceptions import HashingError, InvalidHashError, VerifyMismatchError

from core.config import ph
from logger import setup_logging

from .exceptions import PasswordHashError, PasswordHashingIsError

log = setup_logging()


def hash_password(raw_password: str):
    """Hash raw password using Argon2 algorithm."""
    try:
        return ph.hash(raw_password)
    except HashingError:
        raise PasswordHashingIsError from None
    except Exception as exc:
        raise PasswordHashError from exc


def check_password(raw_password: str, hash_password: str) -> bool:
    """Check whether enter password matches hashed password.

    Arguments:
        raw_password (str): Password entered user.
        hash_password (str): Hash password to compare enter password
        with.

    """
    try:
        ph.verify(hash_password, raw_password)
        return True
    except VerifyMismatchError:
        log.debug("Пароль не совпадает c хешированным паролем")
        return False
    except InvalidHashError:
        log.error("Хэш пустой или имеет неправильную структуру")
        return False
    except Exception as exc:
        log.exception("Произошла неизвестная ошибка при проверке пароля: %s", exc)
        return False
