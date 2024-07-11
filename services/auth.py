from datetime import datetime, timedelta

import jwt


def create_access_token(subject):
    expire = datetime.utcnow() + timedelta(minutes=5)  # from setting
    to_encode = {
        "exp": expire,
        "sub": subject,
        "iss": "api:todo"
    }
    token = jwt.encode(payload=to_encode, key="secret_key_from_settings")
    return token
