from authx.main import AuthX, AuthXConfig
from datetime import timedelta

config = AuthXConfig()
config.JWT_SECRET_KEY = "your_secret_key"
config.JWT_ALGORITHM = "HS256"
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies", "headers"]
config.JWT_COOKIE_SECURE = False
config.JWT_COOKIE_SAMESITE = "lax"
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_ACCESS_COOKIE_PATH = "/"

config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # 24 часа

security = AuthX(config=config)