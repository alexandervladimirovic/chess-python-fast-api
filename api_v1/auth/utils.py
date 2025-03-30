import datetime

import jwt

from core.config import ph, settings


# headers?
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

    to_encode.update(exp=expire, iat=now)

    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


# headers?
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


# exc
def hash_password(raw_password: str):
    """Hash raw password using Argon2 algorithm."""
    return ph.hash(raw_password)


# rehash and exc
def check_password(raw_password: str, hash_password: str) -> bool:
    """Check whether enter password matches hashed password.

    Arguments:
        password (str): Password entered user.
        hash_password (str): Hash password to compare enter password
        with.

    """
    try:
        ph.verify(hash_password, raw_password)
        return True
    except Exception:
        return False
