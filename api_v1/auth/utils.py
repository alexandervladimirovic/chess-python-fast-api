import datetime
import uuid

import jwt
from argon2.exceptions import HashingError, InvalidHashError, VerifyMismatchError

from core.config import ph, settings
from logger import setup_logging

from .exceptions import PasswordHashError, PasswordHashingIsError

log = setup_logging()


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.private_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
    expire_minutes: int = settings.jwt.access_token_expires_in_minutes,
    expire_timedelta: datetime.timedelta | None = None,
):
    """Encode data (payload) in JWT using private key and algorithm.

    Parameters
    ----------
        payload (dict): Data that will be encoded in JWT.
        private_key (str): Private key for signing the JWT.
        algorithm (str): Algorithm for signing JWT.
        expire_minutes (int): Token lifetime in minutes.
        expire_timedelta (timedelta | None): Optional timedelta for setup lifespan
        token.

    Returns
    -------
        str: Encoded JWT as string.

    """
    to_encode = payload.copy()
    now = datetime.datetime.now(tz=datetime.timezone.utc)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + datetime.timedelta(minutes=expire_minutes)

    to_encode.update(
        jti=str(uuid.uuid4()),
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
):
    """Decode JWT using public key and algorithm, verifying signature.

    Parameters
    ----------
        token (str | bytes): JWT for decoding.
        public_key (str): Public key for verifying the JWT signature.
        algorithm (str): Algorithm for verifying JWT signature.

    Returns
    -------
        Decoded data (payload) from the JWT.

    """
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )
    return decoded


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
