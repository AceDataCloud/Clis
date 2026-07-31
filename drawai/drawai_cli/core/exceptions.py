"""Custom exceptions for DrawAI CLI."""


class DrawAIError(Exception):
    """Base exception for DrawAI CLI."""

    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(message)


class DrawAIAuthError(DrawAIError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class DrawAIAPIError(DrawAIError):
    """API error with HTTP status code."""

    def __init__(
        self,
        message: str = "API request failed",
        code: str = "api_error",
        status_code: int | None = None,
    ):
        self.status_code = status_code
        super().__init__(message, code)


class DrawAITimeoutError(DrawAIError):
    """Request timeout error."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
