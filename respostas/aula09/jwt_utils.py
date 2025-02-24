from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

JWT_SECRET_KEY = '196afbce3ae97c9ecddc9660f6d5523f680f8d3a10fb2c7276d6d5af57272553'
JWT_ALGORITHM = 'HS256'
ISSUER = 'localhost'
AUDIENCE = 'localhost'
JWT_SECONDS_TO_EXPIRE = 5 * 60


def create_jwt(
    user_id: str, other_data: dict[str, Any] | None = None, expires_secs: int = 300
) -> str:
    payload: dict[str, Any] = {} if other_data is None else other_data.copy()

    issued_at = datetime.now(tz=timezone.utc)
    expiration = issued_at + timedelta(seconds=expires_secs)

    payload.update({
        'sub': user_id,
        'iss': ISSUER,
        'iat': issued_at,
        'exp': expiration,
        'aud': AUDIENCE,
    })

    encoded_jwt = jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def validate_jwt(token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={'require': ['sub', 'iss', 'iat', 'exp', 'aud']},
            issuer=ISSUER,
            audience=AUDIENCE,
        )
        return payload
    except jwt.exceptions.InvalidTokenError:
        return None


if __name__ == '__main__':
    # new_jwt = create_jwt('jloc@cesar.org.br')
    # print(new_jwt)

    # modificar o JWT com o jwt.io e verificar cada tipo de erro de validação e ir incrementando as exceções
    new_jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqbG9jQGNlc2FyLm9yZy5iciIsImlzcyI6ImxvY2FsIiwiaWF0IjoxNzM5ODg3MDI1LCJleHAiOjE3Mzk4ODczMjUsImF1ZCI6ImxvY2FsaG9zdCJ9.0ThbVF0qa2xBr5ta3CqeFdOYnwVUe6o8Zx-dZBUniiw'

    decoded_jwt = jwt.decode(new_jwt, options={'verify_signature': False})
    print(decoded_jwt)
    jwt_headers = jwt.get_unverified_header(new_jwt)
    print(jwt_headers)
    validated_payload = validate_jwt(new_jwt)
    print(validated_payload)
