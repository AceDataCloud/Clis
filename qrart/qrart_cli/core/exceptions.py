"""Custom exceptions for QRArt CLI."""


class QRArtError(Exception):
    """Base exception for QRArt CLI."""

    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(message)


class QRArtAuthError(QRArtError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class QRArtAPIError(QRArtError):
    """API error with HTTP status code."""

    def __init__(
        self,
        message: str = "API request failed",
        code: str = "api_error",
        status_code: int | None = None,
    ):
        self.status_code = status_code
        super().__init__(message, code)


class QRArtTimeoutError(QRArtError):
    """Request timeout error."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
