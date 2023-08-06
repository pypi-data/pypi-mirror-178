from typing import List


class QmQuaException(Exception):
    pass


class OpenQmException(QmQuaException):
    pass


class FailedToExecuteJobException(QmQuaException):
    pass


class FailedToAddJobToQueueException(QmQuaException):
    pass


class CompilationException(QmQuaException):
    pass


class JobCancelledError(QmQuaException):
    pass


class ErrorJobStateError(QmQuaException):
    def __init__(self, *args, error_list: List[str]):
        super().__init__(*args)
        self._error_list = error_list if error_list else []

    def __str__(self):
        errors_string = "\n".join(error for error in self._error_list)
        return f"{super().__str__()}\n{errors_string}"


class UnknownJobStateError(QmQuaException):
    pass


class InvalidStreamMetadataError(QmQuaException):
    pass


class ConfigValidationException(QmQuaException):
    pass


class ConfigSerializationException(QmQuaException):
    pass


class InvalidConfigError(QmQuaException):
    pass
