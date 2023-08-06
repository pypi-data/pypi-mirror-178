from typing import Any


class RangeException(Exception):
    def __int__(self, message: Any = None):
        super(RangeException, self).__int__(message)


class CredentialsError(Exception):
    def __int__(self, message: Any = None):
        super(CredentialsError, self).__int__(message)


class NotEnoughDataError(Exception):
    def __int__(self, message: Any = None):
        super(NotEnoughDataError, self).__int__(message)
