import jwt

from ..config.settings import settings


def encode_jwt(
    payload,
    private_key: str = settings.AUTH_JWT.private_key_path.read_text(),
    algorithm: str = settings.AUTH_JWT.algorithm,
):
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str,
    public_key: str = settings.AUTH_JWT.public_key_path.read_text(),
    algorithm: str = settings.AUTH_JWT.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded
