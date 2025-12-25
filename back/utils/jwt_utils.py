# import jwt
# import datetime
# from back.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES

# def create_access_token(user_id: str) -> str:
#     """Создание JWT токена"""
#     expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     payload = {
#         "sub": user_id,
#         "exp": expire,
#         "iat": datetime.datetime.utcnow(),
#         "type": "access"
#     }
    
#     return jwt.encode(
#         payload, 
#         JWT_SECRET_KEY, 
#         algorithm=JWT_ALGORITHM
#     )

# def decode_access_token(token: str):
#     """Декодирование JWT токена"""
#     try:
#         payload = jwt.decode(
#             token, 
#             JWT_SECRET_KEY, 
#             algorithms=[JWT_ALGORITHM]
#         )
#         return payload
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.InvalidTokenError:
#         return None