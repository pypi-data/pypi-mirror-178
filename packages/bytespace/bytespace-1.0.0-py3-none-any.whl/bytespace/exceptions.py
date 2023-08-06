
class BaseInterfaceException(Exception):
    def __init__(self, message="An unexpected exception occurred during interface management!"):
        self.message = message
        super().__init__(self.message)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, msg):
        self._message = msg

    @message.getter
    def message(self):
        return self._message

    def __str__(self):
        return f"{self.message}"


class InvalidAppIDError(BaseInterfaceException):
    def __init__(self, message="Application ID provided does not belong to a valid bytespace application!"):
        super().__init__(message)


class MissingPasswordParameterError(BaseInterfaceException):
    def __init__(self, message="Interface requires a password parameter that was not supplied!"):
        super().__init__(message)


class MissingUsernameParameterError(BaseInterfaceException):
    def __init__(self, message="Interface requires a username parameter that was not supplied!"):
        super().__init__(message)


class InvalidTokenError(BaseInterfaceException):
    def __init__(self, message="The token given, or returned, is invalid!"):
        super().__init__(message)
