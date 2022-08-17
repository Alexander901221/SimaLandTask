import jwt
from datetime import datetime, timedelta

JWT_SECRET = 'Bearer'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 120


async def get_token(user_id: int):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return jwt_token
