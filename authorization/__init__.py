import typing
from datetime import datetime, timezone, timedelta

import jwt

secret = "12343242342"


def generate_jwt(user_id):
    return jwt.encode({"exp": datetime.now(tz=timezone.utc) + timedelta(minutes=15), "sub": user_id}, secret, algorithm="HS256")


def decode_jwt(token: str) -> typing.Union[None, int]:
    try:
        token = jwt.decode(token, secret, algorithms=["HS256"])
    except:
        return None

    return token.get('sub')
