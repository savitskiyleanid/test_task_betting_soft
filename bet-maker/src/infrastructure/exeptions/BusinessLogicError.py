class BusinessLogicError(Exception):
    """
    Taken from django.core.exceptions.ValidationError.
    """

    def __init__(
        self,
        message: str | dict | None = None,
        code: str | None = None,
    ):
        if message is None:
            message = 'Что-то пошло не так, обратитесь в поддержку.'

        super().__init__(message)

        self.code = code
        self.error_list: list[str] = []

        if isinstance(message, dict):
            for field, messages in message.items():
                if isinstance(messages, list):
                    self.error_list.extend(messages)
                else:
                    self.error_list.append(messages)
        elif isinstance(message, list):
            self.error_list.extend(message)
        else:
            message = str(message)
            self.error_list.append(message)

        self.message = message

    def __str__(self) -> str:
        return str(self.message)

    def __repr__(self) -> str:
        return f'BusinessLogicError({self.message})'
