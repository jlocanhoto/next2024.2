from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pydantic import BaseModel

JWT_SECRET_KEY = '196afbce3ae97c9ecddc9660f6d5523f680f8d3a10fb2c7276d6d5af57272553'
JWT_ALGORITHM = 'HS256'
JWT_SECONDS_TO_EXPIRE = 5 * 60


class Token(BaseModel):
    access_token: str
    token_type: str


def create_jwt(
    user_id: str, other_data: dict[str, Any] | None = None, expires_secs: int = 300
) -> str:
    payload: dict[str, Any] = {} if other_data is None else other_data.copy()

    issued_at = datetime.now(tz=timezone.utc)
    expiration = issued_at + timedelta(seconds=expires_secs)

    payload.update({
        'sub': user_id,
        'iss': 'localhost',
        'iat': issued_at,
        'exp': expiration,
        'aud': 'localhost',
    })

    encoded_jwt = jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


new_jwt = create_jwt('jloc@cesar.org.br')
print(new_jwt)
