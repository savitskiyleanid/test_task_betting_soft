from src.infrastructure.exeptions.BusinessLogicError import BusinessLogicError


class AuthenticationError(BusinessLogicError):
    """Ошибка аутентификации пользователя."""

    def __init__(self, message: str | None = None, code: str | None = None):
        super().__init__(message=message, code=code)
