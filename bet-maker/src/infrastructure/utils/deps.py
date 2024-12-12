from datetime import datetime

from config.config import settings
from config.database import get_db
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from src.applications.user import UserService
from src.domain.DTO.user import TokenPayload
from src.domain.models.user import User
from src.infrastructure.exeptions.AuthenticationError import \
    AuthenticationError

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="api/v1/login", scheme_name="JWT")


async def get_current_user(token: str = Depends(reuseable_oauth)):
    async with get_db() as session:
        service = UserService(session)
    try:
        payload = jwt.decode(
            token, settings.jwt.JWT_PRIVATE_KEY, algorithms=[settings.jwt.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise AuthenticationError("Токен истек", code="token_expired")
    except (jwt.JWTError, ValidationError):
        raise AuthenticationError(
            "Не удалось подтвердить учетные данные", code="invalid_credentials"
        )

    user = await service.get_user(User, int(token_data.sub))
    if user is None:
        raise AuthenticationError(
            "Не удалось найти пользователя", code="user_not_found"
        )

    return user[0]
