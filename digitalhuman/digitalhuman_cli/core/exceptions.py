"""Custom exceptions for Digital Human CLI."""


class DigitalHumanError(Exception):
    """Base exception for Digital Human CLI."""

    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(message)


class DigitalHumanAuthError(DigitalHumanError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class DigitalHumanAPIError(DigitalHumanError):
    """API error with HTTP status code."""

    def __init__(
        self,
        message: str = "API request failed",
        code: str = "api_error",
        status_code: int | None = None,
    ):
        self.status_code = status_code
        super().__init__(message, code)


class DigitalHumanTimeoutError(DigitalHumanError):
    """Request timeout error."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
