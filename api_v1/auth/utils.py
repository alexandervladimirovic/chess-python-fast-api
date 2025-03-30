import jwt

from core.config import ph, settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.jwt.privave_key_path.read_text(),
    algorithm: str = settings.jwt.algorithm,
) -> str:
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
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )
    return str(encoded)


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


def hash_password(raw_password: str) -> str:
    """Hash raw password using Argon2 algorithm."""
    return str(ph.hash(raw_password))
